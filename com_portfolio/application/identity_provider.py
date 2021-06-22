from abc import ABC, abstractmethod
from uuid import UUID


class IdentityProviderInterface(ABC):

    @abstractmethod
    async def get_user_id(self, access_token: str) -> UUID:
        """
        Provides a user_id by the access_token
        if the token is invalid raises InvalidAccessToken
        """
