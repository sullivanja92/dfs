# NFL DFS Lineup Optimizer

## Overview
This is an NFL DFS lineup optimization package written in python and facilitating lineup optimization from player statistics contained in a pandas [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). <br/>
Currently-supported fantasy sites include **DraftKings** and **FanDuel**.

## Installation
TODO

## Usage

### Import test 2020 data
`from dfs.data import load_2020_data`<br/>
`data = load_2020_data(weeks=[1])`<br/>
`print(data.columns)`

### Create lineup optimizer instance
`from dfs.optimize import LineupOptimizer`<br/>
`optimizer = LineupOptimizer(data=data, points_col='dk_points', salary_col='dk_salary')`

### Add constraints

#### Only include specified teams
`optimizer.set_only_include_teams(teams=['CHI', 'DET', 'GB', 'MIN'])`<br/>

#### Exclude specified teams
`optimizer.set_exclude_teams(teams=['DAL', 'NYG', 'PHI', 'WAS'])`<br/>

#### Include a specified player
`optimizer.set_must_include_player(name='Aaron Rodgers')`<br/>

#### Exclude a specified player
`optimizer.set_exclude_player(name='Mitch Trubisky')`<br/>

#### Add stacks
`optimizer.set_qb_receiver_stack(team='SF')`<br/>

#### Clear current constraints
`optimizer.clear_constraints()`

### Generate lineup
`lineup = optimizer.optimize_lineup(site='dk')`<br/>
`print(lineup)`

## TODO
* Add additional fantasy sites
