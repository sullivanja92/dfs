from abc import ABC, abstractmethod
from typing import Callable


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
    def filter_function(self) -> Callable:
        """
        Returns a callable that may be used to filter the player dataframe based on this slate.

        :return: the callable that may be used to filter the dataframe.
        """
        raise NotImplementedError()
