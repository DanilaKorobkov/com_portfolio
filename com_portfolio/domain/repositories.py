from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Portfolio


class PortfolioRepositoryInterface(ABC):

    @abstractmethod
    async def find_all(self, user_id: UUID) -> tuple[Portfolio, ...]:
        """
        Finds all portfolios owned by a User with the passed user_id,
        returns tuple() if the user has no portfolios
        """

    @abstractmethod
    async def find(self, user_id: UUID, label: str) -> Portfolio:
        """
        Tries to find a portfolio owned by a User with the passed user_id
        and with passed label
        if it doesn't work raises a UserHasNoPortfolio
        """
