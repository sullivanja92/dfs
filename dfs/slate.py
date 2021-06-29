from abc import ABC, abstractmethod

import pandas as pd


class GameSlate(ABC):
    """
    Abstract class used to specify a slate of games that are to be considered for a lineup.
    """

    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of this game slate.

        :return: the slate name.
        """
        raise NotImplementedError()

    @abstractmethod
    def filter_function(self, row: pd.Series, label: str, *args) -> bool:
        """
        Returns a bool that may be used to filter the player dataframe based on this slate.

        :param row: the player dataframe row
        :param label: the dataframe's datetime column
        :param args: a list of args (used in Monday/Thursday NFL slate for week-related args)
        :return: the bool indicating whether or not a row should be included based on this slate.
        """
        raise NotImplementedError()
