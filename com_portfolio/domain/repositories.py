from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Portfolio


class PortfolioRepositoryInterface(ABC):

    @abstractmethod
    async def find(self, user_id: UUID) -> Portfolio:
        """
        Tries to find a portfolio owned by a User with the passed user_id
        if it doesn't work raises a UserHasNoPortfolio
        """
