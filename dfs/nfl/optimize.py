import logging
from abc import ABCMeta
from typing import Dict, Tuple, Union

import pandas as pd

from dfs.nfl import constraints as nfl_constraints
from dfs.nfl import slate
from dfs.nfl.positions import QB, RB, WR, TE, DST, ORDER_DICT
from dfs.optimize import LineupOptimizer
from dfs.site import Site

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class NflLineupOptimizer(LineupOptimizer, metaclass=ABCMeta):
    """
    An abstract subclass of LineupOptimizer containing NFL-specific constraints.
    """

    def player_order_dict(self) -> Dict[str, int]:
        return ORDER_DICT

    def set_qb_receiver_stack(self, team: str, position: str = None, num_receivers: int = None) -> None:  # TODO: make specified team optional
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
        self._add_constraint(nfl_constraints.QbReceiverStackConstraint(team=team,
                                                                       position=position,
                                                                       num_receivers=num_receivers,
                                                                       team_col=self._team_col,
                                                                       position_col=self._position_col))

    def set_rb_dst_stack(self, team: str) -> None:  # TODO: make specified team optional
        """
        Specifies that an optimized lineup should include a RB/DST stack from a given team.

        :param team: the team name
        :return: None
        :raises: ValueError if team name is invalid
        """
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(nfl_constraints.RbDstStackConstraint(team=team,
                                                                  team_col=self._team_col,
                                                                  position_col=self.position_col))

    def set_game_slate_sunday(self) -> None:
        """
        Sets the optimizer to include all Sunday games only.

        :return: None
        """
        logger.info('Setting game slate to "Sunday"')
        self.set_game_slate(slate=slate.NflSundayGameSlate())

    def set_game_slate_sunday_early(self) -> None:
        """
        Sets the optimizer to include only Sunday early games (13PM EST).

        :return: None
        """
        logger.info('Setting game slate to "Sunday early"')
        self.set_game_slate(slate=slate.NflSundayEarlyGameSlate())

    def set_game_slate_sunday_early_and_late(self) -> None:
        """
        Sets the optimizer to include only Sunday early and late games (13PM and 16PM EST).

        :return: None
        """
        logger.info('Setting game slate to "Sunday early and late"')
        self.set_game_slate(slate=slate.NflSundayEarlyAndLateGameSlate())

    def set_game_slate_sunday_and_monday(self) -> None:
        """
        Sets the optimizer to include games taking place on Sunday and Monday.

        :return: None
        """
        logger.info('Setting game slate to "Sunday and Monday"')
        self.set_game_slate(slate=slate.NflSundayAndMondayGameSlate())

    def set_game_slate_monday(self) -> None:
        """
        Sets the optimizer to include games taking place on Monday.

        :return: None
        """
        logger.info('Setting game slate to "Monday"')
        self.set_game_slate(slate=slate.NflMondayGameSlate())

    def set_game_slate_monday_and_thursday(self) -> None:  # TODO: DK only?
        """
        Sets the optimizer to include games taking place on Monday of week n and Thursday of week n+1.

        :return: None
        """
        logger.info('Setting game slate to "Monday and Thursday"')
        weeks = tuple(self.data[self.week_col].unique())
        if len(weeks) != 2:
            raise ValueError('DataFrame must contain two weeks in order to use Monday/Thursday slate')
        self.set_game_slate(slate=slate.NflMondayAndThursdayGameSlate())


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


class YahooNflLineupOptimizer(NflLineupOptimizer):  # TODO: implement single game
    """
    A lineup optimizer for Yahoo salary cap-based NFL lineup optimization.
    """

    def num_players(self) -> int:
        return 9

    def salary_cap(self) -> int:
        return 200

    def site_name(self) -> str:
        return 'Yahoo'

    def position_constraints(self) -> Dict[str, Tuple[int, int]]:
        return {
            QB: (1, 1),
            RB: (2, 3),
            WR: (3, 4),
            TE: (1, 2),
            DST: (1, 1)
        }


def optimizer_factory(site: Site, data: Union[pd.DataFrame, str]) -> NflLineupOptimizer:
    """
    Return a lineup optimizer for a particular DFS site.

    :param site: the DFS site.
    :param data: the optimizer data source.
    :return: an NflLineupOptimizer for the given site.
    """
    return {
        Site.DRAFTKINGS: DraftKingsNflLineupOptimizer(data_source=data, points_col='dk_points', salary_col='dk_salary'),
        Site.FANDUEL: FanDuelNflLineupOptimizer(data_source=data, points_col='fd_points', salary_col='fd_salary'),
        Site.YAHOO: YahooNflLineupOptimizer(data_source=data, points_col='yh_points', salary_col='yh_salary')
    }.get(site, None)
