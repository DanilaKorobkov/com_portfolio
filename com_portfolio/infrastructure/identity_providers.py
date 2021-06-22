from uuid import UUID

import attr

from com_portfolio.application import (
    IdentityProviderInterface,
    InvalidAccessToken,
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class FakeIdentityProvider(IdentityProviderInterface):
    _user_id_by_token: dict[str, UUID] = attr.Factory(dict)

    async def get_user_id(self, access_token: str) -> UUID:
        try:
            return self._user_id_by_token[access_token]
        except KeyError as e:
            raise InvalidAccessToken from e
