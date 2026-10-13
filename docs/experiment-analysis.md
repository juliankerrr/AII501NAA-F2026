#Experiment Analysis

## Variables

The experiments varied:

- simulation count: 10, 50, 100, and 500
- random seed: 1 through 5

##Results

The results are stored in `data/mcts_results.csv`.

## Observations

The simulator didnt always pick the same move. Different random seeds produced different moves, especially with less simulations.

With more simulations, some moves were more consistent, but the chosen move could still change because the rollout policy is random.

## Explanation

The differences are caused by random move selection during simulation. Increasing the number of simulations gives the algorithm more information and can make the results more stable, but it doesnt completely remove randomness.

## Limitation

This experriment varied simulation count and random seed. The utility function, expansion node count, and tree height were not independently configurable in the current basic implementation.
