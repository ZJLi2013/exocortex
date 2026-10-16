---
url: https://sgs-rl.github.io/
fetched: 2026-10-16
title: "A Balanced Data Diet: Addressing the Exploration Bottleneck in Mega-Scale RL for Robot Control"
---

SGS
HighlightsSummaryOverviewMethodResultsClipsBibTeX
<https://arxiv.org/abs/2610.12465> Paper ↗Code (coming soon)Menu

SGSSuccess-GuidedSampling

# A Balanced Data Diet: Addressing the Exploration Bottleneck in Mega-Scale RL for Robot Control

Octi Zhang1,2*Mateo Guaman Castro1*Patrick Yin1*Ignacio Dagnino1Abhishek Gupta1Rosario Scalise1†Byron Boots1†

1University of Washington2NVIDIA*Equal contribution†Equal advising

CoRL 2026<https://arxiv.org/abs/2610.12465> Paper ↗Code (coming soon)

## Highlights

All videos at 1×

UR5e, NutHardware

Highlights

All videos at 1×

UR5eHardware

- 01Nut

- 02Nut

- 03Gear mesh

- 04Gear mesh

- 05Rod

UR5eSimulation

- 06Rod

- 07BNC connector

- 08Waterproof connector

FrankaSimulation

- 09Nut

ANYmal CSimulation

- 10Several terrains

ANYmal DSimulation

- 11Climbing box

- 12Floating island

- 13Stepping stones

## Summary

Success-Guided Sampling (SGS) trains on the task configurations that are neither too easy nor too hard for the current policy. With it, reinforcement learning scales much more effectively, to over a million simulated robots at once, in legged locomotion and contact-rich manipulation.

## Overview

### Locomotion

A single policy, trained from scratch, takes ANYmal C and D across every terrain, from stepping stones to floating islands.

ANYmal C, several terrains

ANYmal D, floating island

ANYmal D, stepping stones

ANYmal D, climbing box

### Manipulation

UR5e and Franka learn per-task contact-rich assembly from the NIST task board, with zero demonstrations and the same reward function across all tasks.

UR5e, rod

UR5e, BNC connector

UR5e, gear mesh

Franka, nut

### Real world

Trained only in simulation, the UR5e assembles parts on the real task board from RGB images, zero-shot.

UR5e, nut

UR5e, rod

UR5e, gear mesh

### Scale

SGS keeps improving as parallel environments grow to a million, where uniform sampling and other methods fall behind.

## Method

### 01The change to PPO

SGS is standard PPO with a small outer loop. It changes only which task configuration an environment resets to.

PPO

- 1initialize policy π

-

- 2for each iteration:

- 3for each environment, in parallel:

- 4if its episode ended:

-

- 5reset to a task configuration drawn uniformly

- 6step π, store the transition

- 7update π with PPO

PPO with SGS

- 1initialize policy π

- 2fix N task configurations, each with an empty history buffer

- 3for each iteration:

- 4for each environment, in parallel:

- 5if its episode ended:

- 6record its success in that task configuration’s history buffer

- 7reset to a task configuration drawn weighted by success rate (SGS)

- 8step π, store the transition

- 9update π with PPO

added changed

### 02Task configurations

A task configuration is a triple (s0, g, e): the robot’s initial state s0, its goal g, and the environment e, such as the terrain type or the layout of the scene. SGS samples a large, fixed set of task configurations before training.

For assembly, the task configurations come in equal parts from three reset strategies.

Franka, nut on boltSimulation

01Reaching
The nut starts anywhere in the workspace, next to the gripper but not always in it, so the robot may have to fetch it first.

02Stable Grasp

03Near-Goal

### 03Sampling during training

We follow one fixed task configuration of each UR5e task through the course of training. SGS gives it small weight while the policy never solves it, large weight when it’s getting better but not perfect, and small weight again once the policy has mastered it.

Nut on boltRod in holeGear meshBNC connectorWaterproof connectorRectangular peg

Iteration 2,8000 of 64 successes

Nut on bolt: one task configuration, 64 trials per checkpoint, with the 95% Wilson interval and the SGS weight relative to its peak

| Iteration

| Successes

| 95% interval

| SGS weight

| 0

| 0 of 64

| 0%–6%

| 0.14

| 1,000

| 0 of 64

| 0%–6%

| 0.14

| 1,800

| 0 of 64

| 0%–6%

| 0.14

| 2,800

| 0 of 64

| 0%–6%

| 0.14

| 3,800

| 9 of 64

| 8%–25%

| 0.83

| 4,000

| 27 of 64

| 31%–54%

| 0.99

| 4,200

| 51 of 64

| 68%–88%

| 0.90

| 4,400

| 52 of 64

| 70%–89%

| 0.88

| 4,600

| 57 of 64

| 79%–95%

| 0.79

| 5,400

| 59 of 64

| 83%–97%

| 0.73

Results

UR5e

ManipulationHardware, Simulation

Nut

Rod

Gear mesh

BNC connector

Waterproof connector

Franka

ManipulationSimulation

Nut

ANYmal C

LocomotionSimulation

Across terrains

ANYmal D

LocomotionSimulation

Climbing box

Stepping stones

### 01Scaling

With SGS, success keeps rising as the number of parallel environments grows to a million. The baselines stall or collapse.

SGSPLRUniformLinear curriculum

LocomotionANYmal D, all terrains

Success rate

Locomotion, success rate, mean of three seeds with 95% confidence interval

| Method

| 4K

| 32K

| 256K

| 1M

| SGS

| 0.46 ± 0.02

| 0.49 ± 0.11

| 0.72 ± 0.05

| 0.73 ± 0.01

| PLR

| 0.00 ± 0.00

| 0.13 ± 0.01

| 0.55 ± 0.14

| 0.54 ± 0.13

| Uniform

| 0.00 ± 0.00

| 0.42 ± 0.04

| 0.00 ± 0.00

| 0.00 ± 0.00

| Linear

| 0.00 ± 0.00

| 0.32 ± 0.03

| 0.00 ± 0.00

| 0.00 ± 0.00

ManipulationFranka, nut-and-bolt assembly

Success rate

Manipulation, success rate, mean of three seeds with 95% confidence interval

| Method

| 4K

| 32K

| 256K

| 1M

| SGS

| 0.00 ± 0.01

| 0.06 ± 0.01

| 0.10 ± 0.14

| 0.70 ± 0.19

| PLR

| 0.00 ± 0.00

| 0.00 ± 0.00

| 0.02 ± 0.04

| 0.05 ± 0.11

| Uniform

| 0.00 ± 0.00

| 0.00 ± 0.00

| 0.01 ± 0.04

| 0.06 ± 0.13

### 02Real world

Trained only in simulation, the UR5e runs on the real task board from RGB images, zero-shot.

#### Nut on bolt

#### Rod in hole

### 03Continuous runs

#### Nut on bolt, Franka, simulation

#### All terrains, ANYmal C, simulation

#### Gear mesh, UR5e, real world

## Clips

### UR5eReal world

#### Nut on bolt

#### Rod in hole

#### Gear mesh

### UR5eSimulation

Nut on bolt

Rod in hole

Gear mesh

BNC connector

Waterproof connector

Rectangular peg

### ANYmal CSimulation

All terrains

Climbing box

Stepping stones

Gap

Balancing beam

Contour

Floating island

Inverted slope

Jump box

Parallel boxes

Pit

Radiating beam

Stairs

### ANYmal DSimulation

Climbing box

Stepping stones

Gap

Balancing beam

Contour

Floating island

Inverted slope

Jump box

Maze

Parallel boxes

Pit

Radiating beam

Stairs

### FrankaSimulation

#### Nut on bolt

## BibTeX

@inproceedings{zhang2026balanced,
title = {A Balanced Data Diet: Addressing the Exploration Bottleneck in Mega-Scale RL for Robot Control},
author = {Zhang, Octi and Guaman Castro, Mateo and Yin, Patrick and
Dagnino, Ignacio and Gupta, Abhishek and Scalise, Rosario and
Boots, Byron},
booktitle = {Conference on Robot Learning (CoRL)},
year = {2026}
}
Copy

SGSSuccess-GuidedSampling

If you want to adapt this website or use its videos, see the Terms of Use.
