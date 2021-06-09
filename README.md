# NFL DFS Lineup Optimizer

## Overview
This is an NFL DFS lineup optimization package written in python and facilitating salary cap-based lineup optimization from player statistics contained in a pandas [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). <br/>
Currently-supported fantasy sites include **DraftKings**, **FanDuel** and **Yahoo** (multi-game slates only).

## Installation
TODO

## Usage

### Import test 2020 data
`from dfs.data import load_2020_data`<br/><br/>
`data = load_2020_data(weeks=[1])`<br/>
`print(data.columns)`

### Create lineup optimizers
`from dfs.optimize import DraftKingsNflLineupOptimizer, FanDuelNflLineupOptimizer, YahooNflLineupOptimizer`<br/><br/>
`dk_optimizer = opt.DraftKingsNflLineupOptimizer(data=data, points_col='dk_points', salary_col='dk_salary')`<br/>
`fd_optimizer = opt.FanDuelNflLineupOptimizer(data=data, points_col='fd_points', salary_col='fd_salary')`<br/>
`yh_optimizer = opt.YahooNflLineupOptimizer(data=data, points_col='yh_points', salary_col='yh_salary')`<br/>

### Add constraints

#### Only include specified teams
`dk_optimizer.set_only_include_teams(teams=['CHI', 'DET', 'GB', 'MIN'])`<br/>

#### Exclude specified teams
`dk_optimizer.set_exclude_teams(teams=['DAL', 'NYG', 'PHI', 'WAS'])`<br/>

#### Include a specified player
`dk_optimizer.set_must_include_player(name='Aaron Rodgers')`<br/>

#### Exclude a specified player
`dk_optimizer.set_exclude_player(name='Mitch Trubisky')`<br/>

#### Add stacks
`dk_optimizer.set_qb_receiver_stack(team='SF')`<br/>

#### Clear current constraints
`dk_optimizer.clear_constraints()`

### Generate lineup
`lineup = dk_optimizer.optimize_lineup()`<br/>
`print(lineup)`

## TODO
* Add additional fantasy sites
* Add game schedule-related constraints
* Implement yahoo single game optimization
* Configure logging
