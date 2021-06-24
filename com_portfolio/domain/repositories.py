from abc import ABC, abstractmethod

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
        and with passed label
        if it doesn't work raises a UserHasNoPortfolio
        """
