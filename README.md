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

    * 1/4: Tzeentchian Scroll, +3 Tzeentch Corruption
    * 1/2: One Physical Reward of your choice
    * 1/8: Rare -> VeryRare upgrade Token
    * 1/8: Streak Recovery + Roll for another Rare Reward
* VeryRare
    * On first unlock: Moleskin + Pen
    * (5%) Void rest of Rewards + Jester Hat (Choice disabled after first obtain)
    * Always: Rare Item
    * Always: Double Coinflip for Rare Item
    * Always: Double Coinflip for Uncommon Item
    * Always: Coinflip for Common Item (3x)

    * 1/3: Legendary Tzeentchian Artifact, +10 Tzeentch Corruption
    * 1/3: Legendary Arcane Artifact, +10 Arcane Corruption
    * 1/3: Legendary Necromantic Artifact, +10 Necromantic Corruption

##### Physical Activity
This should have a type of adventurer / fantasy hero theme going.

Rewards:
* Common
    Always: Triple Coinflip for a common item with one optional reroll if you do 10 pushups, +1 Token if hit without reroll if you do pushups

    * 1/3: 4 Bronze Adventurer Tokens
    * 1/3: 1 Advanced Adventurer Token
        * Silver Token (96%)
        * Golden Token (4%)
    * 1/6: Triple Coinflip for an uncommon item with one optional reroll if you do 10 pushups
    * 1/6: Double Coinflip for a common item with one optional reroll if you do 10 pushups
* Uncommon:
    * Always: Lore / Worldbuilding
    * Always: New Quest / Replace current quest with new one, Coinflip for (bonus quest progress | harder quest with better rewards)
    * Always: Triple Coinflip for a uncommon item with one optional reroll if you do 10 pushups, +1 Token if hit without reroll if you do pushups
    * Always: Physical Challenge

    * 1/3: 1x 3C+1RR for Common reward roll + 4 Bronze Adventure Tokens
    * 1/3: Adventure Token Shop
    * 1/3: 2x 3C+1RR for Common reward roll
* Rare: 
    * Always: Triple Coinflip for a rare item with one optional reroll if you do 10 pushups, +1 Token if hit without reroll if you do pushups

    * 1/4: Khorne Challenge, +3 Khorne Corruption
    * 1/2: Physical Reward of your choice
    * 1/8: Rare -> VeryRare Upgrade Token
    * 1/8: Streak Recovery + Roll for another Rare reward
* VeryRare:
    * On first unlock: Physical Reward
    * (5%) Void rest of Rewards + Jester Hat (Choice disabled after first obtain)
    * Always: Rare Item
    * Always: 3Coin+1RR for Rare Item
    * Always: 3Coin+1RR for Uncommon item
    * Always: 3x 1Coin for Common Item

    * 1/3: Legendary Khorne Challenge, +10 Khorne Corruption
    * 1/3: Legendary Champion's Challenge, +10 Fame
    * 1/3: Legendary Warrior Challenge, +10 Rage

##### Psychonautics
This should be like space explorer theme where I explore my own mind and conscious experience.

Insights represent things like facts, artifacts and the like, anything that gives you a broader understanding of the mind you are exploring.
* Common
    * Always: Quadruple Coinflip, get common item on 3, coinflip for uncommon item if you get 4 heads

    * 1/3: 4 Insights
    * 1/3: 1 Eldrich Insight, +2 Eldritch Corruption
    * 1/6: Quadruple Coinflip for uncommon item on 3 heads, 1d50 for Very Rare Reward
    * 1/6: Quadruple Coinflip for common item on 2, 1d50 for Very Rare Reward
* Uncommon
* Rare
* VeryRare