from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Portfolio


class PortfolioRepositoryInterface(ABC):

    @abstractmethod
    async def find_all(self) -> tuple[Portfolio, ...]:
        """
        Finds all portfolios owned by a User with USER_ID context var,
        returns tuple() if the user has no portfolios
        """

    @abstractmethod
    async def find(self, label: str) -> Portfolio:
        """
        Tries to find a portfolio owned by a User with USER_ID context var
        and with passed label, if there is no a portfolio with the same label
        raises a MissingPortfolioLabel
        """

    @abstractmethod
    async def add(self, label: str) -> UUID:
        """
        Creates a portfolio owned by a User with USER_ID context var
        with passed label or override exists, returns portfolio id
        """
