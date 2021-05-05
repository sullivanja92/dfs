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
`optimizer.set_only_include_teams(teams=['CHI', 'DET', 'GB', 'MIN'])  # only include NFC North teams for consideration`<br/>
`optimizer.set_exclude_teams(teams=['DAL', 'NYG', 'PHI', 'WAS'])  # exclude NFC East teams from consideration`<br/>
`optimizer.set_must_include_player(name='Aaron Rodgers')  # ensure that Aaron Rodgers is included in the optimized lineup`<br/>
`optimizer.set_exclude_player(name='Mitch Trubisky')  # ensure that Mitch Trubisky is excluded from the optized lineup`<br/>
`optimizer.set_qb_receiver_stack(team='SF')  # ensure that the optimized lineup includes a qb/receiver stack from San Francisco`<br/>
`optimizer.clear_constraints()  # clear any constraints for this optimizer`

### Generate lineup
`lineup = optimizer.optimize_lineup(site='dk')`<br/>
`print(lineup)`

## TODO
* Add additional fantasy sites
