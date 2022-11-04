# Gordian
A bot using [python-sc2](https://github.com/BurnySc2/python-sc2) for playing [Starcraft 2](https://starcraft2.com/en-us/) using [sc2 api](https://github.com/Blizzard/s2client-api).

## Gordian's aspirations
- [ ] speed mining
- [ ] basic 2 base CIA timing
- [ ] tighten up pre-moving workers to building locations (esp early ones, maybe reserve a worker)
- [ ] honorable greeting and surrender
- [ ] defend worker rushes
- [ ] build order flexibility / pivoting
  - [ ] separation of core build and match-up specific adaptations
- [ ] scouting
- [ ] responding to scouting information (expanding vs production)
  - [ ] going all in / macroing up














- [ ] responding to scouting information (tech and counters)
  - [ ] proportional responses
- [ ] drops (zealots, dts)
  - [ ] warp prism juggling (giraffe, immortals, adepts??)
- [ ] ability value (force-field, storm, feedback, blink, charge, etc.)
- [ ] army tactics
  - [ ] army splitting
  - [ ] concavity
- [ ] squad tactics
  - [ ] one-shotting
  - [ ] anticipating splash damage
  - [ ] target priority (iterative)
  - [ ] oracle micro
  - [ ] formations
- [ ] map control
  - [ ] enemy army awareness
  - [ ] end-game vision (trade efficiency, map control, army composition)
- [ ] test the opponent–what would be difficult to code?

## AI strategy research
- Belief, Desire, Intention system
- Goal-Oriented Action Plan
- MCTS algorithm
  - Monte Carlo Tree Search
  - reinforcement learning
  - consider possibilities, focusing on ones we think are good already (exploration vs exploitation)
  - MCTS plays out the game using a "forward model", a simplified abstraction of the game logic
  - Four steps
    - Selection: build a tree of possible states around current state, selecting promising states to a fixed depth
    - Expansion: not clear
    - Simulation: random decisions from this point to a win/loss/timeout
    - Backpropagation: use the score of the random line to update the score of every decision node in the tree
    - repeat 1000s of times, then make a decision
  - MCTS algorithms often shift emphasis around on the tree during the selection phase to Explore more
  - Anytime algorithm which can stop making these random walks when time resources are limited
  - more here on Total War Rome II: https://youtu.be/1m9-7ZrpbBo
  - optimizations
    - can prune the tree of obviously bad moves
    - can also group together similar sets of choices whose order don't really matter if they are all made
- Classical planning
  - build order systems

## Exploring MCTS for macro strategy
- state:
  - what buildings are complete/underway for each player
  - how many workers for each player
  - how many bases are controlled by each player
  - what and how many units are controlled by each player
  - what technologies are researched by each player
- decisions: how to use current resources?
  - build buildings
  - build units
  - build workers
  - research upgrades
  - save them until the next decision opportunity
- 

## To download
`git clone --recursive https://github.com/Duncan/gordian`

## To run the bot vs ingame ai
`python gordian main.py`

## To publish for ladder
tbd

## To get coding assistance in PyCharm
Mark python-sc2 directory as source root.

## Documentation 
tbd
