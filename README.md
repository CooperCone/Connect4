# Connect 4

## Description

This project is a collection of files that let you play and test various ai implementations of the Connect 4 game. You can use this project in two ways: play an interactive game or test ai in multiple games.

## Dependencies

- Python 3
- No others!

## Basic Usage

It's recommended that you run all code for this project from the Python repl.

    py
    >>> from main import *
    >>> game = Game(ManualStrategy(), ManualStrategy())
    >>> game.play()

This will begin a basic 2 player game where each player inputs the column where they'd like to insert a piece. When creating the Game object, the first two parameters are the strategies used by the red and blue players respectively. The red player always goes first.

### Strategies

If you'd like to play against the ai, or pit two ai against each other, you will need to create different strategies. All possible strategies live in the strategies.py file.

    py
    >>> from main import *
    >>> game = Game(ManualStrategy(), MinimaxStrategy(4, runHeuristic))
    >>> game.play()

The MinimaxStrategy is currently the main ai used. It has two required parameters, depth and value heuristic. The depth refers to the maximum depth the minimax algorithm is able to explore. The value heuristic is the heuristic used to determine how valuable a given board position is.

### Value Heuristics

Value heuristics are functions that determine how valuable a given board position is, where positive values are good and negative values are bad. Their range is [-1e50 and 1e50] There are currently two value heuristics: win and run. Win simply returns a good value if the position is a winner, a bad value if the position is a loser, and 0 otherwise.

An improved heuristic is run, which counts all the runs that each player has and returns a weighted sum, where longer runs are weighted with a higher absolute value.

### Logging

If you'd like to see what the game is doing during its run, you can create a logging object. Currently, there are only two: FileLogger and NoLogging, where NoLogging is the default.

    py
    >>> from main import *
    >>> loggingStrategy = FileLogger('game.log')
    >>> game = Game(ManualStrategy(),
        MinimaxStrategy(4, runHeuristic, logging=loggingStrategy),
        logging=loggingStrategy)
    >>> game.play()

## Evaluation Usage

Along with the ability to play games against the ai, this system also includes a monte-carlo simulator and evaluation framework that lets you compare different algorithms or algorithm modifications.

### Test Sets

In order to evaluate the quality of an agent, we have the ability to generate a series of starting board positions. This lets us run many simulations instead of simply running a single head to head test from an empty board.

**Note**: This api is likely to change very soon

    py generateTrainingSet.py > fileName.test

In the file, cases to generate specifies the number of test cases and turnDistribution specifies the range of turns to do in each test case. Currently, the test cases are generated randomly. This is also most likely to change.

### Simulator

To start a simulation, you must first add the strategies that you want to test. The simulation will create an n-way comparison, where each strategy plays each other strategy in both red and blue positions. These individual simulations are called runs. When starting the simulation, you must specify a file name to load the dataset.

    py
    >>> from evaluate import *
    >>> simulator = Simulator()
    >>> simulator.addStrategy("Random", RandomStrategy(seed=5))
    >>> simulator.addStrategy("Minimax", MinimaxStrategy(4, winHeuristic))
    >>> simulator.simulate('fileName.test', lambda x: [])

The second parameter to the simulate function is a function that returns metric reporting criteria.

### Metrics

Each game that is run generates a series of metrics for each strategy. All metrics are listed below:

| Metric Name | Description |
| ----------- | ----------- |
| Time        | Length of time that each turn took |
| Win         | 1 if the strategy won, 0 otherwise |
| Loss        | 1 if the strategy lost, 0 otherwise |

After these metrics are generated, we can combine them accross all simulations and strategies tested to gain insight into which strategies are best.

The format of these metrics stored on each strategy is called a MetricMap. This map is a dictionary that maps the metric names to lists of metric values. (It's a list for standardization. For metrics like win/loss, it's just a list of one value).

### Report Generation

After the metrics are created, the simulator creates a report that is displayed for each strategy tested. To generate the report, the metrics undergo three transformations:

- Generation of report values that will be displayed.
- Combination of report values across different runs.
- Conversion to string for displaying.

An example is for the Average Turn Timer metric. 

- First, we generate the report value. For each run and each game, we have a list of times that each turn took. We combine these lists into a larger list of lists. We then take the median of each of the inner lists. This leaves us with a list of values, where each value is the median turn time taken in a game. We then average this list to create the final report metric for this run. This process is performed for both red and blue players.
- Now that we have the Average Turn Timer report value for each strategy on each run, we must collect them accross all runs. Let's assume we have 3 strategies that are collected into the following runs:

  - Random vs Minimax(4)
  - Minimax(4) vs Random
  - Random vs Minimax(5)
  - Minimax(5) vs Random
  - Minimax(4) vs Minimax(5)
  - Minimax(5) vs Minimax(4)

  We then collect each strategy for a given side and combine its Average Turn Timer report metric. In this case, we will collect both the Random Red players into a single set of metrics. We then average their values for Average Turn Timer. This is performed for all strategies for a given side. We then display each strategy and the metrics that were chosen for both red and blue sides.
- Finally, we can convert this value to a string. Since we end with a float, we can do a simple string conversion and round to the nearest 4th decimal place.

In code, this would look like:

    py
    >>> from evaluate import *
    >>> simulator = Simulator()
    >>> simulator.addStrategy("Random", RandomStrategy(seed=5))
    >>> simulator.addStrategy("Minimax", MinimaxStrategy(4, winHeuristic))
    >>> metricGeneration = lambda metrics: [
      metric_create("Average Turn Timer",
        lambda reportMetric: f"{reportMetric:.4f}",
        metric_avg,
        metric_avg(
          metric_map(
            metric_collect(metrics, "time"),
            metric_median
          )
        )
      )
    ]
    >>> metrics = simulator.simulate('fileName.test', metricGeneration)
    >>> simulator.printSimulationResults(metrics)

The format for the metric combinations are fairly complex, but I'll go through some of the necesities. The metric generation parameter is a function that takes as input the metrics that were output from the games played for a given run. The return value is a list of report metrics. Each report metric must return a tuple generated from the metric_create function. It takes a few inputs: 1) name of the metric, 2) function to convert the final metric to a string, 3) function to combine the report value from different runs, and 4), function to convert the base metric reported from the game to the report value.
