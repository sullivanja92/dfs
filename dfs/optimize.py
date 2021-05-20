import csv
from collections.abc import Mapping
from typing import AbstractSet, List, Union, Iterator

import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

from dfs import constraints
from dfs import file_utils
from dfs import positions, data_frame_utils, pulp_utils
from dfs import sites
from dfs.exceptions import InvalidDataFrameException, UnsolvableLineupException, InvalidConstraintException


class OptimizedLineup:
    """
    A class that represents an optimized fantasy football lineup for a given site.
    """

    def __init__(self, optimizer: 'LineupOptimizer', site: str):
        """
        :param optimizer: The optimizer used to generate this lineup.
        :param site: The fantasy site that the lineup has been generated for.
        """
        self.site = site
        players = optimizer.data[optimizer.data.apply(lambda x: x['LpVariable'].varValue == 1, axis=1)]
        self.points = round(players[optimizer.points_col].sum(), 2)
        self.salary = players[optimizer.salary_col].sum()
        col_mapping = {
            optimizer.id_col: 'id',
            optimizer.name_col: 'name',
            optimizer.position_col: 'position',
            optimizer.team_col: 'team',
            optimizer.points_col: 'points',
            optimizer.salary_col: 'salary'
        }
        players_dict = players.to_dict('records')
        for p in players_dict:
            for k, v in col_mapping.items():
                p[v] = p.pop(k)
            keys_to_delete = []
            for k in p.keys():
                if k not in col_mapping.values():
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del p[k]
        self.players = [LineupPlayer(p) for p in players_dict]

    def write_to_file(self, file_path: str) -> None:
        """
        Writes the optimized lineup to a CSV file.

        :param file_path: the path to the file which will be created if it does not exist.
        :return: None
        :raises: ValueError if file_path is None or points to a non-CSV file.
        """
        if file_path is None:
            raise ValueError('File path cannot be none')
        extension = file_utils.get_extension(file_path)
        if extension != 'csv':
            raise ValueError(f"Only CSV output is supported, found: {extension}")
        file_exists = file_utils.file_exists(file_path)
        with open(file_path, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=self.players[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.players)

    def __repr__(self):
        return f"dfs.optimize.OptimizedLineup(site={self.site}, points={self.points}, salary={self.salary}, players={self.players})"

    def __str__(self):
        players_string = '\n'.join([f"{p['position'].value} - {p['name']} {p['points']} @ {p['salary']} salary"
                                    for p in self.players])
        return (f"Optimized {self.site} Lineup \n"
                f"{self.points} points @ {self.salary} salary \n") + players_string


class LineupPlayer(Mapping):  # TODO: improve this class
    """
    A model of a player included in an optimized lineup.
    """

    def __len__(self) -> int:
        return len(vars(self))

    def __iter__(self) -> Iterator[str]:
        return iter({a: getattr(self, a) for a in vars(self)})

    def keys(self) -> AbstractSet[str]:
        return vars(self).keys()

    def __init__(self, player_dict):
        """
        :param player_dict: the player dict from dataframe
        """
        self.name = player_dict['name']
        self.position = player_dict['position']
        self.team = player_dict['team']
        self.points = player_dict['points']
        self.salary = player_dict['salary']

    def __getitem__(self, item):
        return getattr(self, item)


class LineupOptimizer:
    """
    A pandas data frame-based fantasy football lineup optimizer.
    This class is used to generate optimal fantasy football lineups for various sites when provided
    a data frame containing player, position, salary and points information.
    """

    def __init__(self,
                 data_source: Union[pd.DataFrame, str],
                 id_col: str = 'id',
                 name_col: str = 'name',
                 points_col: str = 'points',
                 position_col: str = 'position',
                 salary_col: str = 'salary',
                 team_col: str = 'team'):
        """
        :param data_source: A dataframe or file path containing fantasy data.
        :param id_col: The player ID column. Default is 'id'.
        :param name_col: The player name column. Default is 'name'.
        :param points_col: The fantasy points column. Default is 'points'.
        :param position_col: The player position column. Default is 'position'.
        :param salary_col: The player salary column. Default is 'salary'.
        :param team_col: The player team column. Default is 'team'.
        """
        if type(data_source) is pd.DataFrame:
            self._data = data_source.copy()  # don't impact original dataframe
        elif type(data_source) is str:
            if not file_utils.file_exists(file=data_source):
                raise ValueError('The data source file does not exist!')
            extension = file_utils.get_extension(file_path=data_source)
            if extension == 'csv':
                self._data = pd.read_csv(filepath_or_buffer=data_source)
            elif extension == 'xlsx':
                self._data = pd.read_excel(io=data_source)
            else:
                raise ValueError('Invalid data source file path! csv and xlsx are supported.')
        else:
            raise ValueError('Invalid data source type!')
        if not all(c in self._data.columns for c in [id_col, name_col, points_col, position_col, salary_col, team_col]):
            raise ValueError('DataFrame does not contain necessary columns')
        self._id_col = id_col
        self._name_col = name_col
        self._points_col = points_col
        self._position_col = position_col
        self._salary_col = salary_col
        self._team_col = team_col
        self._constraints = []
        self._data[self._position_col] = self._data[self._position_col].apply(lambda x: positions.normalize_position(x))
        self._data.dropna(subset=[self._points_col, self._salary_col], inplace=True)  # TODO: include more columns?

    @property
    def data(self):
        return self._data

    @property
    def id_col(self):
        return self._id_col

    @property
    def name_col(self):
        return self._name_col

    @property
    def points_col(self):
        return self._points_col

    @property
    def position_col(self):
        return self._position_col

    @property
    def salary_col(self):
        return self._salary_col

    @property
    def team_col(self):
        return self._team_col

    def set_only_include_teams(self, teams: List[str]) -> None:
        """
        Sets the teams that are to be considered for the lineup optimization.

        :param teams: The list of teams to consider.
        :return: None
        :raises: ValueError if teams to include is none or empty.
        """
        if teams is None or len(teams) == 0:
            raise ValueError('Included teams must not be none or empty')
        self._add_constraint(constraints.OnlyIncludeTeamsConstraint(teams=teams,
                                                                    team_column=self._team_col))

    def set_exclude_teams(self, teams: List[str]) -> None:
        """
        Sets the list of teams whose players are to be excluded from lineup optimization.

        :param teams: The list of teams to exclude.
        :return: None
        :raises: ValueError if teams to exclude is none or empty.
        """
        if teams is None or len(teams) == 0:
            raise ValueError('Teams to exclude must not be none or empty')
        for team in teams:
            self.set_max_players_from_team(n=0, team=team)

    def set_must_include_team(self, team: str):
        """
        Specifies that a lineup must include a player from a given team.

        :param team: The team that the lineup must include.
        :return: None
        :raises: ValueError if team is none or not found in data frame.
        """
        self.set_min_players_from_team(n=1, team=team)

    def set_must_include_player(self, **kwargs) -> None:
        """
        Specifies that a lineup must include a player identified by either name or id.
        Either name or id must be provided in kwargs.

        :return: None
        :raises: ValueError if the player is None or not found in the dataframe
        """
        if all([it not in kwargs for it in ['id', 'name']]):
            raise ValueError('Must provide id or name')
        key, col = (kwargs['id'], self._id_col) if 'id' in kwargs else (kwargs['name'], self.name_col)
        if key is None or key not in self._data[col].unique():
            raise ValueError(f"{key} not found in data frame's {col} column")
        self._add_constraint(constraints.IncludePlayerConstraint(player=key,
                                                                 name_col=col))

    def set_exclude_player(self, **kwargs) -> None:
        """
        Specifies that a lineup must exclude a player identified by name.

        :return: None
        :raises: ValueError if player is None or not found in dataframe
        """
        if all([it not in kwargs for it in ['id', 'name']]):
            raise ValueError('Must provide id or name')
        key, col = (kwargs['id'], self._id_col) if 'id' in kwargs else (kwargs['name'], self.name_col)
        if key is None or key not in self._data[col].unique():
            raise ValueError(f"{key} not found in data frame's {col} column")
        self._add_constraint(constraints.ExcludePlayerConstraint(player=key,
                                                                 name_col=col))

    def set_num_players_from_team(self, n: int, team: str):
        """
        Sets the number of players from a team that an optimized lineup must include.

        :param n: the number of players
        :param team: the team name
        :return: None
        :raises: ValueError if number of players or team are invalid
        """
        if n is None or all([n > s.num_players() for s in list(sites.Site)]):
            raise ValueError('Invalid number of players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.MaxPlayersFromTeamConstraint(maximum=n,
                                                                      team=team,
                                                                      team_col=self._team_col))
        try:
            self._add_constraint(constraints.MinPlayersFromTeamConstraint(minimum=n,
                                                                          team=team,
                                                                          team_col=self._team_col))
        except InvalidConstraintException:
            self._constraints.pop()  # remove max players constraint if this one fails
            raise

    def set_max_players_from_team(self, n: int, team: str) -> None:
        """
        Sets the maximum number of players that can be included in an optimized lineup from a particular team.

        :param n: the maximum number of players that can be included from a particular team
        :param team: the name of the team
        :return: None
        :raises: ValueError if maximum or team are invalid
        """
        if n is None or n < 0:
            raise ValueError('Invalid maximum players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.MaxPlayersFromTeamConstraint(maximum=n,
                                                                      team=team,
                                                                      team_col=self._team_col))

    def set_min_players_from_team(self, n: int, team: str) -> None:
        """
        Sets the minimum number of players from a given team that must be included in an optimized lineup.

        :param n: the minimum number of players from the specified team that must be included
        :param team: the name of the team
        :return: None
        :raises: ValueError if minimum or team are invalid
        """
        if n is None or all([n > s.num_players() for s in list(sites.Site)]):
            raise ValueError('Invalid minimum number of players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        if n == 0:
            return
        self._add_constraint(constraints.MinPlayersFromTeamConstraint(minimum=n,
                                                                      team=team,
                                                                      team_col=self._team_col))

    def set_max_salary(self, n: int) -> None:
        """
        Sets the maximum salary that can be used in an optimized lineup.

        :param n: the max salary.
        :return: None
        :raises: ValueError if maximum is invalid
        """
        if n is None or n <= 0:
            raise ValueError('Invalid maximum')
        self._add_constraint(constraints.MaxSalaryCapConstraint(salary=n,
                                                                salary_col=self._salary_col))

    def set_min_salary(self, n: int) -> None:
        """
        Sets the minimum salary that can be used in an optimized lineup.

        :param n: the minimum salary
        :return: None
        :raises: ValueError if minimum is invalid
        """
        if n is None or all([n > s.salary_cap() for s in list(sites.Site)]):
            raise ValueError('Invalid minimum')
        self._add_constraint(constraints.MinSalaryCapConstraint(salary=n,
                                                                salary_col=self._salary_col))

    def set_qb_receiver_stack(self, team: str) -> None:
        """
        Specifies that an optimized lineup should include a QB/receiver stack from a given team.

        :param team: the team name
        :return: None
        :raises: ValueError if team name is invalid
        """
        if team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.QbReceiverStackConstraint(position_col=self._position_col,
                                                                   team=team,
                                                                   team_col=self._team_col))

    def set_rb_def_stack(self, team=None) -> None:
        raise NotImplementedError()

    def _add_constraint(self, constraint: constraints.LineupConstraint) -> None:
        """
        Internal method used to add a constraint by first checking if it is valid.

        :param constraint: The constraint to add.
        :return: None
        :raises: InvalidConstraintException if the constraint is not valid
        """
        is_valid, message = constraint.is_valid(self._constraints)
        if is_valid:
            self._constraints.append(constraint)
        else:
            raise InvalidConstraintException(f"Invalid constraint: {message}")

    def clear_constraints(self) -> None:
        """
        Clears the current lineup optimizer constraints.

        :return: None
        """
        self._constraints = []

    def optimize_lineup(self, site: Union[sites.Site, str]) -> OptimizedLineup:
        """
        Generates and returns an optimized lineup for a given fantasy football site.
        The lineup is generated using the class's data variable and is optimized under provided constraints.

        :param site: The fantasy site to generate a lineup for. Can be of type Site or str (full or abbreviation).
        :return: The optimized lineup.
        :raises: ValueError, InvalidDataFrameException
        """
        if (type(site) is str and site.lower() in ('draftkings', 'dk')) or site == sites.Site.DRAFTKINGS:
            site = sites.Site.DRAFTKINGS
        elif (type(site) is str and site.lower() in ('fanduel', 'fd')) or site == sites.Site.FANDUEL:
            site = sites.Site.FANDUEL
        else:
            raise ValueError('The provided fantasy site is invalid')
        position_constraints = site.position_constraints()
        if not data_frame_utils.col_contains_all_values(self._data, self.position_col, position_constraints.keys()):
            raise InvalidDataFrameException('Data frame is missing required positions')
        self._data['LpVariable'] = self._data.apply(lambda x: LpVariable(f"{x[self._position_col]}_{x.name}", cat='Binary'), axis=1)
        problem = LpProblem(f"{site.name()} Lineup Optimization", LpMaximize)
        for k, v in position_constraints.items():
            players = self._data[self._data[self._position_col] == k]
            problem += lpSum(players['LpVariable']) >= v[0]
            problem += lpSum(players['LpVariable']) <= v[1]
        problem += lpSum(self._data[self._points_col] * self._data['LpVariable'])
        problem += constraints.LineupSizeConstraint(site.num_players()).apply(self._data)[0]
        problem += constraints.MaxSalaryCapConstraint(site.salary_cap(), self._salary_col).apply(self._data)[0]
        for constraint in self._constraints:
            for c in constraint.apply(self._data):  # stack-related constraints may return multiple from apply()
                problem += c
        problem.solve(PULP_CBC_CMD(msg=False))
        if not pulp_utils.is_optimal_solution_found(problem):
            raise UnsolvableLineupException('No optimal solution found under current lineup constraints')
        return OptimizedLineup(self, site.name())
