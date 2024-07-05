# ProgressPal
## Introduction
A gamification system for long term motivation and goalsetting

## Design Document
There are two types of problems that ProgressPal aims to solve:
* Habit building and maintenance
* (Short / Medium / Long) term goal setting and motivation
    * In particular for projects that are not immediately rewarding

The core idea is that we have two types of reward mechanisms, an experience system that is roughly speaking a weighted tracker for how many tasks are done and a currency system that gives more concrete rewards and can be exchanged for (real life) rewards.

I think the best way to develop this kind of system is to be quite organic with it, first track most things manually as and write python utility that does the book keeping. As ideas get tested and the better ones stick I can then build out a more sophisticated interface (maybe in godot to make multiplatforming easy).

### Goals, Tasks and Todos
Any task completed should give experience based on the time it took and its difficulty, but exp is more for a time tracking rather than accomplishment tracking device, it's good to see persistent progress.

The level curve should be exponential and uncapped, I think levels higher than 100 aren't really that desirable and levels above 300 don't feel good at all, maybe we'll even add a prestige system, but that's for later.

### Habits
These should be done regularly and therefore give regular rewards, but instead of just being simple checkbox tracking they should be spiced up with a gambling system, random rewards of different probabilties with potential for very rare big ticket rewards.

Inspired from the way gacha games handle their probabilities the first implementation will have a 50% chance of not yielding any reward, and the remaining 50% are broken down as follows:
* Common: 70%
* Uncommon: 22%
* Rare: 6%
* Very Rare: 2%

In total the probabilities are as follows:
* Nothing: 50%
* Common: 35%
* Uncommon: 11%
* Rare: 3%
* Very Rare: 1%

