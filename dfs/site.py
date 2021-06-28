from enum import Enum


class Site(Enum):
    """
    DFS site enumeration.
    """

    DRAFTKINGS = 0
    FANDUEL = 1
    YAHOO = 2

    def abbreviation(self) -> str:
        """
        Returns the DFS site's abbreviation.

        :return: the DFS site abbreviation.
        """
        return {
            0: 'dk',
            1: 'fd',
            2: 'yh',
        }.get(self.value, None)
