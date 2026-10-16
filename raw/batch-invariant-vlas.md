---
url: https://cyberneticphysics.com/blog/batch-invariant-vlas
fetched: 2026-10-16
title: "Batch-Invariant VLAs"
---

﻿Blog⌈ Talk to us ⌋

⌈ Blog ⌋2026-09-04

# Batch-Invariant VLAs

Numerical divergence in SigLIP, Conv2D, PyTorch dispatch, and batched matrix multiplication.

Published2026-09-04T09:00Z

Revised2026-09-22

Read6 min / 1,260 words

TopicsVLA / PyTorch / Triton / Inference

AuthorsCybernetic Physics

Published2026-09-04T09:00Z

Revised2026-09-22

Read6 min / 1,260 words

TopicsVLA / PyTorch / Triton / Inference

AuthorsCybernetic Physics

Contents

- 01Profiling batch-invariance

- 02Thinky's Ops were not enough

- 03Weird nn.Conv2d behavior

- 04Replacing nn.Conv2d

- 05torch.matmul(a,b) != torch.mm(a,b)

- 06Replacing aten::bmm

- 07Running the tracer after all our changes

- 08Conclusion

- 09References

Contents

- 01Profiling batch-invariance

- 02Thinky's Ops were not enough

- 03Weird nn.Conv2d behavior

- 04Replacing nn.Conv2d

- 05torch.matmul(a,b) != torch.mm(a,b)

- 06Replacing aten::bmm

- 07Running the tracer after all our changes

- 08Conclusion

- 09References

<https://github.com/cybernetic-physics/batch-invariant-pizero> View the code on GitHub
[image: A line chart with no axes. A green trace, labelled batch = 1, runs almost flat from left to right. A white dashed trace, labelled batch = 32, leaves it just past the middle at a point marked with a small square — annotated first divergence — and falls steadily away from it to the right edge.]
The same input at batch = 1 and batch = 32. The traces agree until one kernel picks a different reduction order, and never meet again.

Not many people are thinking about VLA inference servers (yet) but at Cybernetic Physics we definitely are. In the very near future they’ll be powering fleets of robots both in production and during RL training. Non-determinism in VLA inference is expected since it has already been shown to exist in LLM inference [1]. However, non-determinism in VLA inference is particularly insidious because it can be propagated through the action space and affect the robot’s behavior in the real world.

This post describes our debugging journey to make π0 batch-invariant, which is crucial for reliable robot behavior.

π0 [2] is a vision-language-action policy that combines images and robot state with a language-conditioned model, then predicts a chunk of continuous actions through flow matching.

Batch-invariant: batching several requests together must not change the answer for any one of them.

TL;DR: a per-sample SigLIP patch projection and an explicit stack of two-dimensional torch.mm calls were needed in the π0 path. The latter was a way to force the dispatcher to reach the invariant aten::mm implementation (provided by Thinking Machines) instead of silently taking a batched path.

## Profiling batch-invariance

Since floating point precision errors compound throughout the neural network layers, we first want to identify where the numerical divergence first begins, and then trace along the forward activations through the layers.

Before changing any code, we added an opt-in tracer and began recording named tensors along the model path:

pythontrace.py

with trace_context(trace): output = model(**inputs) GLOBAL_TRACE.record("final_action", action)

The tracer recursively detaches and clones tensors, including tensors nested in dictionaries and lists. It moves those snapshots to CPU, then compares the reference tensor (batch_size = 1) with element zero of the batched tensor (batch_size = 32). At each point it reports maximum absolute difference, mean absolute difference, RMSE, relative L2 error, and output magnitude.

Here are the tracer output logs for the SigLIP patch embedding:

trace.json

"input_embeds.selected_image_feature.hidden_states": { "max_abs_diff": 0.0, "mean_abs_diff": 0.0, "rmse": 0.0, "relative_l2_mean": 0.0, "relative_l2_max": 0.0, "output_abs_max": 4.864709377288818},"input_embeds.selected_image_feature.last_hidden_state": { "max_abs_diff": 6.496906280517578e-06, "mean_abs_diff": 1.1066537126680487e-06, "rmse": 1.3891448134017992e-06, "relative_l2_mean": 8.866771281645924e-07, "relative_l2_max": 8.866771281645924e-07, "output_abs_max": 7.3877058029174805},

Each one of these is a named tensor compared between the batched and non-batched runs.

The names preserve the route through the model. For example, the image path records names such as input_embeds.selected_image_feature.patch_embeds and joint-model states under step_0.action_joint_model.layer_{i}.pre_attn. This allows us to find the first diverging (non-zero diff) tensor.
[image: The seven stages of the model path, top to bottom: input, SigLIP patch embedding, vision transformer, joint model / KV cache, action expert, flow integration, final action. Every stage after the input is marked exact. Nothing diverges.]
Fig. 01A perfect deterministic implementation must have zero points of divergence.

After a fix, the same experiment can be rerun. If the earlier tensors are now exact but a later tensor is not, the tracer has done its job. It has moved the investigation to the next actionable boundary.

## Thinky's Ops were not enough

In a recent blogpost [1], Thinking Machines showed that non-determinism in LLM inference is caused by varying batch sizes that change the reduction order in kernels. To fix this, they introduced 4 custom batch-invariant <https://github.com/thinking-machines-lab/batch_invariant_ops> kernels [3] for standard PyTorch ops.

Before changing π0, we enabled the batch-invariant operator mode from Thinking Machines. Their work already provides CUDA implementations whose arithmetic is designed not to change when unrelated batch members are added. In this checkout, the mode uses torch.library and registers:

- aten::mm

- aten::addmm

- aten::_log_softmax

- aten::mean.dim

The important entries for π0 are aten::mm and aten::addmm. Their implementations call a persistent Triton matmul kernel, accumulate output tiles in float32, and use a fixed tile configuration selected by input dtype.

We then reran the same batch experiment. Some differences disappeared, but the action was still not invariant. The tracer painted a picture like the following:
[image: The seven stages of the model path, top to bottom: input, SigLIP patch embedding, vision transformer, joint model / KV cache, action expert, flow integration, final action. Every stage after the input is marked diverged, and the SigLIP patch embedding — the first of them — is annotated as the first divergence.]
Fig. 02With only the batch-invariant operators enabled, everything downstream of the patch embedding still diverges.

All the named tensors diverged, but the first divergence was in the SigLIP patch embedding.

Yay! For a second we were worried that Thinky’s batch-invariant operators were going to be enough and that the project would be easy.

## Weird nn.Conv2d behavior

The tracer pointed to the very beginning of π0’s visual path, SigLIP’s patch embedding. This is the operation that turns an image into tokens. In the configured model, a 224×224 RGB image is split into non-overlapping 14×14 patches, producing (224 / 14)² = 256 image tokens. The original path used nn.Conv2d with 1,152 output channels, a 14×14 kernel, a 14×14 stride, and no padding.

Mathematically, each output patch is independent of every other sample:

y[b, p, o] = Σ x[b, c, hₚ + kₕ, wₚ + k𝓌] · W[o, c, kₕ, k𝓌]
(1)

However, the common implementations of any matmul (which includes convolution) use a reduction over the input channels and kernel positions. The order of that reduction can change when the global shape changes, which can lead to non-deterministic behavior across batches.

After testing the nn.Conv2d kernel on its own, with the same configuration, we found out that it stops being batch-invariant at batch-size 32.

python

Conv2d( in_channels=3, out_channels=1152, kernel_size=(14, 14), stride=(14, 14), padding=(0, 0), padding_mode='zeros', device='cuda')

stdout

batch_size = 1 max abs diff = 0.0batch_size = 2 max abs diff = 0.0batch_size = 4 max abs diff = 0.0batch_size = 8 max abs diff = 0.0batch_size = 16 max abs diff = 0.0batch_size = 32 max abs diff = 0.000902771949...

A “normal” convolution configuration (e.g. using a 3×3 kernel) is batch-invariant, but the SigLIP patch projection is not.

On paper, this should be an easy case. Every output patch depends only on one image, one patch, and one set of weights. But that mathematical independence does not force one fixed GPU reduction order. The convolution implementation can make choices based on the complete input shape.

## Replacing nn.Conv2d

The active SigLIP model now uses _UnfoldConv2d. For each sample it calls F.unfold, flattens the learned kernel, computes a matrix product, adds the bias, and reshapes the result back to (1, channels, patch_height, patch_width) before concatenating samples. It is intentionally straightforward. We wanted the reduction scope to be visible before worrying about performance.

pythonsiglip/patch_embed.py

for sample in x: patches = F.unfold(sample.unsqueeze(0), ...) output = flattened_weight @ patches + bias[:, None] outputs.append(output.reshape(1, -1, height, width))return torch.cat(outputs, dim=0)

### What about a custom Triton implementation?

We also explored writing a specialized Triton implementation. It maps each program to an output element, decodes width, height, channel, and sample indices, then performs a fixed reduction over input channels and kernel positions. It masks out-of-range reduction elements and padded spatial loads, accumulates in a Triton accumulator, adds bias, and stores one output element.

Stay tuned for our next post where we will be going over the Triton implementation in more detail!

## torch.matmul(a,b) != torch.mm(a,b)

The new _UnfoldConv2d implementation successfully restored batch-invariance to the SigLIP patch projection. However, the tracer then pointed to a new divergence in the joint model, in the attention path.
[image: The seven stages of the model path, top to bottom: input, SigLIP patch embedding, vision transformer, joint model / KV cache, action expert, flow integration, final action. The SigLIP patch embedding and the vision transformer are marked exact; the joint model / KV cache and everything after it are marked diverged, and the joint model / KV cache is annotated as the first divergence.]
Fig. 03After the patch-projection fix, the first divergence moves into the joint model's attention path.

This time, nothing looked suspicious. All operators used the batch-invariant package (aten::mm, aten::addmm, aten::_log_softmax, and aten::mean.dim). So the error must be in the dispatch path.

Adding more internal logging steps for the tracer to check, it seems like the divergence begins at the final matrix multiplication of the joint model.

python

attn_output = torch.matmul(attn_weights, value_states) GLOBAL_TRACE.record( f"step_0.action_joint_model.layer_{layer_idx}" ".pre_attn.attn_output_pre", attn_output,)

But wait. Shouldn’t Thinky’s batch-invariant aten::mm have been used here? The answer is no.

torch.matmul is shape-dependent, and it does not always dispatch to the same operator as torch.mm.

With two-dimensional inputs, torch.matmul reaches aten::mm. With higher-rank inputs, it treats the leading dimensions as batches and reaches aten::bmm. The Python call looks similar, but the profiler shows a different dispatch path:

torch.profiler

# attn_weights = torch.randn(4, 281, device='cuda')# value_states = torch.randn(281, 256, device='cuda') Name Self CPU % Self CPU CPU tot % CPU total CPU avg Self CUDA CUDA % CUDA total CUDA avg #------------ ---------- -------- --------- --------- -------- --------- ------ ---------- -------- -aten::matmul 0.05% 21.280us 99.99% 46.617ms 46.617ms 0.000us 0.00% 31.353us 31.353us 1aten::mm 76.89% 35.848ms 99.94% 46.596ms 46.596ms 4.479us 100.00% 31.353us 31.353us 1 # attn_weights = torch.randn(32, 8, 4, 281, device='cuda')# value_states = torch.randn(32, 8, 281, 256, device='cuda') Name Self CPU % Self CPU CPU tot % CPU total CPU avg Self CUDA CUDA % CUDA total CUDA avg #------------ ---------- -------- --------- --------- -------- --------- ------ ---------- --------- -aten::matmul 0.14% 64.853us 99.99% 47.305ms 47.305ms 0.000us 0.00% 211.712us 211.712us 1aten::bmm 75.93% 35.922ms 99.69% 47.166ms 47.166ms 26.464us 100.00% 211.712us 211.712us 1

| Input shapes

| Expression

| Profiler event

| What this means

| (4, 281) × (281, 256)

| torch.matmul(a, b)

| aten::matmul → aten::mm

| The invariant aten::mm replacement can run.

| (32, 8, 4, 281) × (32, 8, 281, 256)

| torch.matmul(a, b)

| aten::matmul → aten::bmm

| The aten::mm replacement is bypassed.

Using the torch profiler, we can see the actual operations being performed. The same torch.matmul call reaches aten::mm for rank-2 inputs but aten::bmm for rank-4 inputs.

## Replacing aten::bmm

### Simple looped solution

A simple looped solution would be to treat the first two dimensions as independent batch-like indices and performs a genuine two-dimensional multiplication for every pair:

python

def loop_bmm(a, b): return torch.stack([ torch.stack([ torch.mm(a[i][j], b[i][j]) for j in range(a.shape[1]) ]) for i in range(a.shape[0]) ])

### Using vmap

Using vmap(torch.mm) sounds promising, until you realise that vmap requires special registration using torch.library.register_vmap.

That basically means that vmap is not a magic solution that will automatically work for all functions. It needs to be explicitly implemented for our new aten::mm implementation. However, if we do torch.vmap(torch.mm)(a, b) anyway, it would simply dispatch the existing aten::bmm implementation, which is not what we want.

A custom batch-invariant aten::bmm implementation for vmap will be explored in a future blogpost.

## Running the tracer after all our changes

results.json

{ "batch_size": 32, "reference_samples": 1, "distractor_samples": 31, "num_trials": 1, "reference_seconds": 1.2700269939377904, "batch_seconds_mean": 23.618852018378675, "throughput_speedup_vs_reference": 1.7206959836314306, "metrics_mean": { "max_abs_diff": 0.0, "mean_abs_diff": 0.0, "rmse": 0.0, "relative_l2_mean": 0.0, "relative_l2_max": 0.0, "output_abs_max": 1.0 }, "metrics_worst": { "max_abs_diff": 0.0, "mean_abs_diff": 0.0, "rmse": 0.0, "relative_l2_max": 0.0, "output_abs_max": 1.0 }}

Every single tracked metric, mean and worst case alike, reads exactly 0.0 across the entire batch. Determinism achieved!

## Conclusion

Enabling Thinking Machines’ batch-invariant operators was only the first step. Two things were breaking π0’s batch invariance. First, the SigLIP patch projection failed because the convolution kernel picks a different reduction order once the batch hits 32. The attention product failed because torch.matmul on a rank-4 tensor dispatches to aten::bmm, not aten::mm, so Thinking Machines’ kernel was never called.

The implementation is now correct but slow since we are running each matrix multiplication separately. The next step is a batch-invariant BMM kernel that preserves the same arithmetic.

## References

- 01He, Horace, et al. “Defeating Nondeterminism in LLM Inference.” Thinking Machines Lab, Sep. 2025. thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference

- 02Black, Kevin, et al. “π0: Our First Generalist Policy.” Physical Intelligence, Oct. 2024. pi.website/blog/pi0

- 03Thinking Machines Lab. batch_invariant_ops. GitHub, 2025. <https://github.com/thinking-machines-lab/batch_invariant_ops> github.com/thinking-machines-lab/batch_invariant_ops

## Attribution

The batch-invariant operator approach is based on the work published by Thinking Machines. The model is derived from the open-pi-zero implementation and the π0 architecture described by Physical Intelligence. The implementation uses PyTorch and Triton.

