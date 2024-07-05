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


#### Details
##### Journaling
I think journaling should have a type of magic / wizardry theme, so the currency for this habit are scrolls, every time I complete a morning and evening journal I get a scroll.

Rewards:
* Common
    Always: Double Coinflip for a common item

    * 1/3: 4 Scrolls
    * 1/3: 1 Random Elemental Scroll
        * higher tier scroll, elemental are (fire, earth, water, wind) (24%), void (4%)
    * 1/6: Double Coinflip to Uncommon Item
    * 1/6: Coinflip to Common item
* Uncommon
    * Always: Lore / Worldbuilding
    * Always: Double Coinflip for an Uncommon Item

    * 1/3: Free Spin + (5 scrolls -> 1 Random Elemental Scroll | 8 Scrolls -> 1 Particular Elemental Scroll | 4 Scrolls)
    * 1/3: 1 Random Elemental Scroll + (Coinflip to Common -> Uncommon upgrade token)
    * 1/3: 3 Spins
* Rare
    * Double Coinflip for a Rare Item
    * Always: Unlock a new theme.

    * 1/4: Tzeentchian Scroll
    * 1/2: One Physical Reward of your choice
    * 1/8: Rare -> VeryRare upgrade Token
    * 1/8: (Streak Recovery + Roll for another Rare Reward)
* VeryRare
    * On first unlock: Moleskin + Pen
    * (5%) Void rest of Rewards + Jester Hat (Choice disabled after first obtain)
    * Always: Rare Item
    * Always: Double Coinflip for Rare Item
    * Always: Double Coinflip for Uncommon Item
    * Always: Coinflip for Item (3x)

    * 1/3: Legendary Tzeentchian Artifact, +10 Tzeentch Corruption
    * 1/3: Legendary Arcane Artifact, +10 Arcane Corruption
    * 1/3: Legendary Necromantic Artifact, +10 Necromantic Corruption

##### Physical Activity
For starters this only contains 