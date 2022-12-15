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

## Handling build orders
- have the "core" build order be written super greedy, with only safety measures cannot possibly be attached to a
    scouted enemy state.
- have ALL 
- eventually employ mcts perhaps for "core" build order

## Structure
- **Gordian** is the top level object which inherits from BotAI
- **Interpreter** is a layer which is used to read information from the game state as accessible through the BotAI. It provides interpretations of that information through its properties and methods, and caches its results to avoid redundant calculations.
- **Blackboard** stores bot state information that must be shared between components like the build/train wishlist, build plan, unit assignments, etc.
- **Operations** are where the strategic/decision logic lives. Operations are composed into a tree-like structure with a global operation (for now, `PvXGlobalOp`, eventually the bot will choose between multiple of these global operations based on matchup, previous performance, and an element of randomness) instantiating various sub-operations, which in turn have logic for implementing their own sub-operations, etc. Each operation is assigned a set of units which it is responsible for controlling, and bases its decisions on information about the game state accessed via the Interpreter, bot state information stored on the blackboard, and operation state information stored within the operation instance. The leaves of this tree of Operations (and perhaps some nodes) issue orders to the units assigned to them.

### Outdated:
Generally, actions are carried out by operations. Some operations give orders directly to units, while most operations decide what child operations to initiate, which may in turn give orders to units. There is a global operation (say, PvXOp) which has sub-operations (SpeedMiningOp, TechDevelopmentOp, ScoutingOp, etc.), which in turn have sub operations (SpeedMineBaseLocationOp, TechDevelopmentGroundUpgradesOp, ScoutingHallucinationOp, etc.), which may in turn have sub operations, all the way down to the leaves of the operations tree which issue orders to specific units. The units that a given operation is in charge of (that descendent operations give orders to) are "assigned" to that operation, and cannot be also assigned to a non-descendent operation. Operations' list of children are dynamic according to the logic of the parent op.

Operations do not directly read from the game state–they rely on Interpreters which recognize patterns and calculate conclusions upon which Operations can make their decisions. Examples might include ResourceInvestmentInterpreter (tracks relative investment into economy, tech/upgrades, and production, having sub-Interpreters: EconomyStrengthInterpreter, TechLevelInterpreter, ProductionVolumeInterpreter), CombatResultInterpreter (predicts outcomes of conflicts between friendly and enemy units in an area), IncomingAttackInterpreter (detects attacks that may or may not require defending).

So each operation (at each level) uses Interpreters to understand the game state within that plan's context, implements logic to decide what to do given those understandings, and initiates operations to respond to the situation.

It may make sense to break up operations into multiple phases which segue one into the other when given criteria are met. For instance, BlinkStalkerMainCliffsAttackOp might have BlinkStalkerMainCliffsAttackUnitPreparationOp, BlinkStalkerMainCliffsAttackExecutionOp, and BlinkStalkerMainCliffsAttackRetreatOp. In this case, I think the best way to handle would be to have BlinkStalkerMainCliffsAttackOp have one sub-operation at a time, and contain logic for transitioning from one to the next, while the logic for each phase is baked into the three distinct phase Ops.

Each operation also needs to be able to signal its completion. If an operation should be aborted, that will be made by the parent, as informed by its Interpreters (just as the parent decided to initiate the operation).

Interpreters need to cache the results of their interpretations in the blackboard so that redundant calculations are avoided. They should be cached alongside an iteration stamp after which they should be considered invalid and recalculated. The duration of their validity will depend on the nature of the interpretation (ThreatPriorityInterpreter during a fight will need a faster refresh rate than ProductionVolumeInterpreter for instance)



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
