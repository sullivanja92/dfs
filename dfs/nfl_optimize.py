import logging
from abc import ABCMeta
from typing import Dict, Tuple

from dfs import constraints
from dfs.optimize import LineupOptimizer
from dfs.positions import QB, RB, WR, TE, DST
from dfs.slate import Slate

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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

    def set_game_slate_sunday(self) -> None:
        """
        Sets the optimizer to include all Sunday games only.

        :return: None
        """
        logger.info('Setting game slate to "Sunday"')
        self.set_game_slate(slate=Slate.SUNDAY)

    def set_game_slate_sunday_early(self) -> None:
        """
        Sets the optimizer to include only Sunday early games (13PM EST).

        :return: None
        """
        logger.info('Setting game slate to "Sunday early"')
        self.set_game_slate(slate=Slate.SUNDAY_EARLY)

    def set_game_slate_sunday_early_and_late(self) -> None:
        """
        Sets the optimizer to include only Sunday early and late games (13PM and 16PM EST).

        :return: None
        """
        logger.info('Setting game slate to "Sunday early and late"')
        self.set_game_slate(slate=Slate.SUNDAY_EARLY_AND_LATE)

    def set_game_slate_sunday_and_monday(self) -> None:
        """
        Sets the optimizer to include games taking place on Sunday and Monday.

        :return: None
        """
        logger.info('Setting game slate to "Sunday and Monday"')
        self.set_game_slate(slate=Slate.SUNDAY_AND_MONDAY)

    def set_game_slate_monday(self) -> None:
        """
        Sets the optimizer to include games taking place on Monday.

        :return: None
        """
        logger.info('Setting game slate to "Monday"')
        self.set_game_slate(slate=Slate.MONDAY)


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
