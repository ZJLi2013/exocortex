---
url: https://alpha-nist.github.io/
fetched: 2026-10-16
title: "AlphaNIST"
---

Skip to content

Dark

# AlphaNIST

From AlphaGo to AlphaZero, reinforcement learning produced strategies that surprised expert players. AlphaZero learned from experience at scale, without human demonstrations.

AlphaNIST brings this philosophy to contact-rich, high-precision robotic assembly in simulation. An end-to-end policy learns how to complete the task, without prescribed manipulation stages.

Narrated overview · 4:36

Your browser does not support embedded video. Download the film.

Play2:41

Ten-component assembly.

Close-up

Four successful ten-part runs, using a policy trained separately from the single-component policy below.

## The assembly challenge

[image: A rotating studio view of the NIST board, with yellow movable parts shown fully assembled.]

NIST Assembly Task Board #1, shown fully assembled.

The NIST board has twenty assembly tasks, with parts as small as 4 mm. Fitting one part can take several changes of grasp and orientation. Tight clearances leave little room for error: a tilted nut can jam or cross-thread.

With several parts, the robot also has to choose an order. An installed component may block the gripper’s next move.

## Robots can be creative—if we give them room.

Trying to prescribe every maneuver means anticipating how the robot should respond as contacts and obstructions change. A two-finger gripper may also need solutions quite different from those that come naturally to a human hand.

Perhaps the answer is to stop telling the robot how we think the task should be done, and let it learn how to get there. We give it a binary task reward for success and train it through vast amounts of diverse experience. That leaves room for the robot to discover solutions we might never have thought to teach.

## How the robot learns

### Experience diversity:
heterogeneous assets and initial states

One policy trains across twenty heterogeneous assemblies, starting from loose parts, in-hand grasps, and partial assemblies cached in simulation.

Near-complete starts let the robot practice finishing an assembly before it can solve the whole task. The cache supplies starting states, not demonstrations.

Your browser does not support embedded video. Download the video.

Play0:34

Examples of diverse training starting states

### Success-guided sampling

Beta sampling favors starting states the policy solves about half the time, while giving every state a chance. Progress on one state can make another solvable; its sampling weight then changes with new outcomes.

[image: Success-guided sampling: starting states are selected, data flows into the policy, and success estimates update the sampling weights.]

Starting states receive different amounts of practice as the policy learns. SGS project ↗

## Single-component assembly experiment

Your browser does not support embedded video. Download the film.

Play1:43

One policy performs all twenty assembly tasks, with one component to assemble in each run.

Gears
Nuts
Rods
Pegs
Connectors

With binary task rewards, one policy trained across all twenty tasks reaches higher training success than twenty separate specialists. Adding rewards for reaching and alignment reduces success in this experiment.

[image: Figure 5 comparison: success by task for four training conditions, alongside overall success of 98.2% for a shared policy with binary rewards, 81.4% for separate policies with binary rewards, 17.8% for a shared policy with dense rewards, and 78.3% for separate policies with dense rewards.]

Swipe or scroll horizontally to view the full figure.Training success across varied starting states.

## Emergent assembly behavior

[image: Five successive frames: the robot holds an 8 mm peg at its center, releases it onto the board, grasps near its end, lifts it, and inserts it into its socket.]

The gripper puts down the 8 mm peg and picks it up near one end, leaving more of the peg exposed for insertion.

[image: Five frames show the gripper using the board surface to reorient a waterproof connector before insertion.]

The gripper uses contact with the board to turn the waterproof connector before inserting it.

[image: Five frames show the gripper setting down a D-sub connector and regrasping it for socket alignment.]

The D-sub connector is set down and regrasped to align it with its socket.

[image: Five frames show a medium gear pivoting from a side grasp toward a horizontal pose over its mounting post.]

Held from the side, the medium gear pivots into a horizontal pose above its mounting post.

[image: Five frames show an M12 nut being rolled from its edge onto a flat face and positioned on a bolt.]

The gripper rolls the M12 nut from its edge onto a flat face before placing it on the bolt.

[image: Five frames show successive one-sided fingertip contacts advancing an M4 nut along a bolt.]

One-sided fingertip taps turn the M4 nut along the bolt.

[image: Five frames show a fingertip pushing an 8 mm rod across the surface, followed by grasping and lifting.]

A fingertip pushes the 8 mm rod across the surface before the gripper picks it up.

[image: Five frames show different gripper positions around an M16 nut while fingertip contacts turn the nut along the bolt.]

The gripper moves around the M16 nut, using fingertip contact to turn it along the bolt.

←

→

Alpha NIST
