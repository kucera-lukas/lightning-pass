"""Module containing helper functions to manage vaults."""
from __future__ import annotations

from typing import NamedTuple, Union

from lightning_pass.util import credentials, database
from lightning_pass.util.exceptions import (
    InvalidEmail,
    InvalidURL,
    ValidationFailure,
    VaultException,
)
from lightning_pass.util.validators import EmailValidator


class Vault(NamedTuple):
    """Store all of the data connected to one vault."""

    user_id: int
    platform_name: str
    website: str
    username: str
    email: str
    password: Union[str, bytes]
    vault_index: int


def get_vault(user_id: int, vault_index: int) -> Vault | bool:
    """Return a ``Vault`` tied to the given arguments.

    :param user_id: The user_id connected to the wanted ``Vault``
    :param vault_index: The index of the wanted ``Vault``

    """
    with database.database_manager() as db:
        sql = """SELECT *
                   FROM lightning_pass.vaults
                  WHERE user_id = {}
                    AND vault_index = {}""".format(
            "%s",
            "%s",
        )
        db.execute(sql, (user_id, vault_index))
        result = db.fetchone()

    try:
        return Vault(
            user_id,
            result[2],
            result[3],
            result[4],
            result[5],
            result[6],
            result[7],
        )
    except TypeError:
        return False


def update_vault(vault: Vault) -> None:
    """Update or create a new vault.

    Checks vault values.
    Updates an existing vault if it already exists.
    Creates a new vault if it does not already exist.

    :param vault: The vault data to work with

    :raises InvalidURL: if the vault URL is invalid
    :raises InvalidEmail: if the vault email is invalid
    :raises VaultException: if one (or more) vault fields are empty

    """
    if not (url := credentials.validate_url(vault.website)):
        raise InvalidURL

    # replace website value with a correct url
    vault = Vault(*vault[:2], url, *vault[3:])

    try:
        EmailValidator().pattern(vault.email)
    except ValidationFailure as e:
        raise InvalidEmail from e

    if not all(vault):
        raise VaultException

    if credentials.check_item_existence(
        str(vault.user_id),
        "user_id",
        "vaults",
        should_exist=True,
        second_key=vault.vault_index,
        second_key_column="vault_index",
    ):
        _update_vault(vault)
    else:
        _new_vault(vault)


def delete_vault(user_id: int, vault_index: int) -> None:
    """Delete a vault stored in the database.

    Updates vault indexes as well.

    :param user_id: The of the user tied to the vault which should be deleted
    :param vault_index: The index of the vault

    """
    with database.database_manager() as db:
        # not using f-string due to SQL injection
        sql = """DELETE FROM lightning_pass.vaults
                       WHERE user_id = {}
                         AND vault_index = {}""".format(
            "%s",
            "%s",
        )
        db.execute(sql, (user_id, vault_index))

    with database.enable_db_safe_mode(), database.database_manager() as db:
        # not using f-string due to SQL injection
        sql = """UPDATE lightning_pass.vaults
                    SET vault_index = vault_index - 1
                  WHERE vault_index > {}""".format(
            "%s",
        )
        # expecting a sequence, thus create a tuple with the trailing comma
        db.execute(sql, (vault_index,))


def _update_vault(vault: Vault) -> None:
    """Update an already existing vault."""
    with database.database_manager() as db:
        # not using f-string due to SQL injection
        sql = """UPDATE lightning_pass.vaults
                    SET
                        platform_name = {},
                        website = {},
                        username = {},
                        email = {},
                        password = {}
                  WHERE user_id = {}
                    AND vault_index = {}
        """.format(
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
        )
        db.execute(
            sql,
            (
                vault.platform_name,
                vault.website,
                vault.username,
                vault.email,
                vault.password,
                vault.user_id,
                vault.vault_index,
            ),
        )


def _new_vault(vault: Vault) -> None:
    """Insert a new page into the database"""
    with database.database_manager() as db:
        # not using f-string due to SQL injection
        sql = """
        INSERT INTO lightning_pass.vaults (
        user_id,
        platform_name,
        website,
        username,
        email,
        password,
        vault_index
        )
             VALUES ({}, {}, {}, {}, {}, {}, {})
        """.format(
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
        )
        db.execute(
            sql,
            (
                vault.user_id,
                vault.platform_name,
                vault.website,
                vault.username,
                vault.email,
                vault.password,
                vault.vault_index,
            ),
        )


__all__ = [
    "Vault",
    "delete_vault",
    "get_vault",
    "update_vault",
]
