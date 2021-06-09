from abc import ABCMeta
from typing import Dict, Tuple, Union

import pandas as pd

from dfs import constraints
from dfs.optimize import LineupOptimizer
from dfs.positions import QB, RB, WR, TE, DST


class NflLineupOptimizer(LineupOptimizer, metaclass=ABCMeta):
    """
    An abstract subclass of LineupOptimizer containing NFL-specific constraints.
    """

    # TODO: make specified team optional
    def set_qb_receiver_stack(self, team: str, position: str = None, num_receivers: int = None) -> None:
        """
        Specifies that an optimized lineup should include a QB/receiver stack from a given team.
        The method allows specifying either the receiver position or the number of receivers to include, but not both.

        :param team: the team name
        :param position: the position - WR or TE - to include. This is optional.
        :param num_receivers: the number of receivers to include in the stack.
        :return: None
        :raises: ValueError if team name is invalid
        """
        if team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        if position is not None and num_receivers is not None:  # TODO: should this be supported?
            raise ValueError('Both of "position" and "num_receivers" cannot be provided')
        if position is not None and position not in ['WR', 'TE']:
            raise ValueError(f"The provided position - {position} - is not valid")
        # max_receivers = None  # TODO: implement this when refactoring to optimizers for specific sites
        # if num_receivers > max_receivers:
        #     pass
        self._add_constraint(constraints.QbReceiverStackConstraint(team=team,
                                                                   position=position,
                                                                   num_receivers=num_receivers,
                                                                   team_col=self._team_col,
                                                                   position_col=self._position_col))

    # TODO: make specified team optional
    def set_rb_dst_stack(self, team: str) -> None:
        """
        Specifies that an optimized lineup should include a RB/DST stack from a given team.

        :param team: the team name
        :return: None
        :raises: ValueError if team name is invalid
        """
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.RbDstStackConstraint(team=team,
                                                              team_col=self._team_col,
                                                              position_col=self.position_col))


class DraftKingsNflLineupOptimizer(NflLineupOptimizer):
    """
    A lineup optimizer for DraftKings salary cap-based NFL lineup optimization.
    """

    def num_players(self) -> int:
        return 9

    def salary_cap(self) -> int:
        return 50_000

    def site_name(self) -> str:
        return 'DraftKings'

    def position_constraints(self) -> Dict[str, Tuple[int, int]]:
        return {
            QB: (1, 1),
            RB: (2, 3),
            WR: (3, 4),
            TE: (1, 2),
            DST: (1, 1)
        }


class FanDuelNflLineupOptimizer(NflLineupOptimizer):
    """
    A lineup optimizer for FanDuel salary cap-based NFL lineup optimization.
    """

    def num_players(self) -> int:
        return 9

    def salary_cap(self) -> int:
        return 60_000

    def site_name(self) -> str:
        return 'FanDuel'

    def position_constraints(self) -> Dict[str, Tuple[int, int]]:
        return {
            QB: (1, 1),
            RB: (2, 3),
            WR: (3, 4),
            TE: (1, 2),
            DST: (1, 1)
        }


class YahooNflLineupOptimizer(NflLineupOptimizer):
    """
    A lineup optimizer for Yahoo salary cap-based NFL lineup optimization.
    # TODO: implement single game
    """

    _MULTI_GAME_LINEUP_SIZE = 9
    _MULTI_GAME_CONSTRAINTS = {
        QB: (1, 1),
        RB: (2, 3),
        WR: (3, 4),
        TE: (1, 2),
        DST: (1, 1)
    }
    _SINGLE_GAME_LINEUP_SIZE = 5
    _SINGLE_GAME_CONSTRAINTS = {
        QB: (0, 5),
        RB: (0, 5),
        WR: (0, 5),
        TE: (0, 5),
        DST: (0, 5)
    }
    _SUPERSTAR_MULTIPLIER = 1.5

    def __init__(self,
                 data_source: Union[pd.DataFrame, str],
                 name_col: str = 'name',
                 points_col: str = 'points',
                 position_col: str = 'position',
                 salary_col: str = 'salary',
                 team_col: str = 'team',
                 **kwargs):
        """

        :param data_source:
        :param name_col:
        :param points_col:
        :param position_col:
        :param salary_col:
        :param team_col:
        :param kwargs:
        """
        super().__init__(data_source, name_col, points_col, position_col, salary_col, team_col, **kwargs)
        self._is_single_game = False

    def num_players(self) -> int:
        if self._is_single_game:
            return self._SINGLE_GAME_LINEUP_SIZE
        else:
            return self._MULTI_GAME_LINEUP_SIZE

    def salary_cap(self) -> int:
        return 200

    def site_name(self) -> str:
        return 'Yahoo'

    def position_constraints(self) -> Dict[str, Tuple[int, int]]:
        if self._is_single_game:
            return self._SINGLE_GAME_CONSTRAINTS
        else:
            return self._MULTI_GAME_CONSTRAINTS

    # def set_single_game_contest(self, t1: str, t2: str) -> None:
    #     """
    #
    #     :param t1:
    #     :param t2:
    #     :return:
    #     """
    #     if not self._is_single_game:
    #         if not all(t in self._data[self.team_col].unique() for t in [t1, t2]):
    #             raise ValueError("Team(s) not found in dataframe's team column")
    #         self._is_single_game = True
    #         self._add_constraint(constraints.SingleGameConstraint(t1=t1,
    #                                                               t2=t2,
    #                                                               team_col=self.team_col,
    #                                                               num_players=self._SINGLE_GAME_LINEUP_SIZE))
    #
    # def set_multi_game_contest(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     if self._is_single_game:
    #         self._is_single_game = False
    #         self._constraints = list(filter(lambda c: type(c) is not constraints.SingleGameConstraint,
    #                                         self._constraints))
