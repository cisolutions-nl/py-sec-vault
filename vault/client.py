import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import Mapping, Optional, Union

import requests

from .exceptions import ForbiddenError, InvalidPathError

logger = logging.getLogger(__name__)


@dataclass
class Client(ABC):
    _token: str = field(init=False, repr=False)
    host: str

    def __post_init__(self):
        self._auth()

    def read_secrets(
        self, engine_name: str, vault_path: str
    ) -> Mapping[str, str]:
        """Reads all secrets from vault engine and path.
        :param engine_name: the name of the vault engine;
        :param vault_path: the name of the vault path;
        :return: mapping of secret names to secret values;
        """
        response = requests.get(
            url=f"{self.host}v1/{engine_name}/data/{vault_path}",
            headers={
                "X-Vault-Token": self._token,
            },
        )
        if response.status_code == 404:
            raise InvalidPathError(vault_path=vault_path)
        if response.status_code == 403:
            raise ForbiddenError(
                engine_name=engine_name, vault_path=vault_path
            )
        return response.json()["data"]["data"]

    def _auth(self) -> None:
        """An abstract method for authenticating
        with vault used by subclasses."""
        raise NotImplementedError


@dataclass
class TokenClient(Client):
    token: str = field(repr=False)

    def _auth(self) -> None:
        self._token = self.token


@dataclass
class AppRoleClient(Client):
    role_id: str
    secret_id: str = field(repr=False)

    def _auth(self) -> None:
        response = requests.post(
            url=f"{self.host}v1/auth/approle/login",
            data={
                "role_id": self.role_id,
                "secret_id": self.secret_id,
            },
        )

        self._token = response.json()["auth"]["client_token"]


def get_client(
    host: str,
    token: Optional[str] = None,
    role_id: Optional[str] = None,
    secret_id: Optional[str] = None,
) -> Optional[Union[TokenClient, AppRoleClient]]:
    """Returns a vault client based on the authentication method.
    :param host: the vault host;
    :param token: the vault token;
    :param role_id: the vault role id;
    :param secret_id: the vault secret id;
    :return: a vault client;
    """
    if token:
        logger.info("Authenticating with vault using token.")
        return TokenClient(host=host, token=token)

    if role_id and secret_id:
        logger.info("Authenticating with vault using approle.")
        return AppRoleClient(
            host=host,
            role_id=role_id,
            secret_id=secret_id,
        )
