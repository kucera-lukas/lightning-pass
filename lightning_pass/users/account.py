"""Module containing the Account class and other functions related to accounts."""
from __future__ import annotations

import functools
from datetime import datetime
from typing import TYPE_CHECKING, Generator, TypeVar

import lightning_pass.util.credentials as credentials
import lightning_pass.util.database as database
from lightning_pass.users.vaults import Vault
from lightning_pass.util.exceptions import (
    AccountDoesNotExist,
    EmailAlreadyExists,
    InvalidEmail,
    InvalidPassword,
    InvalidUsername,
    PasswordsDoNotMatch,
    UsernameAlreadyExists,
    ValidationFailure,
)
from lightning_pass.util.validators import (
    EmailValidator,
    PasswordValidator,
    UsernameValidator,
    Validator,
)

if TYPE_CHECKING:
    from lightning_pass.util.credentials import PasswordData


_V = TypeVar("_V", bound=Validator)


class Account:
    """This class holds information about the currently logged in user."""

    username_validator: _V = UsernameValidator()
    password_validator: _V = PasswordValidator()
    email_validator: _V = EmailValidator()

    def __init__(self, user_id: int) -> None:
        """Construct the class.

        :param int user_id: Database primary key ``id`` of the account

        """
        self._user_id = user_id
        self.vault_unlocked = False

    def __repr__(self) -> str:
        """Provide information about this class."""
        return f"{self.__class__.__name__}({self.user_id})"

    @classmethod
    def register(
        cls,
        username: str,
        password: str,
        confirm_password: str,
        email: str,
    ) -> Account:
        """Secondary class constructor for registering.

        :param str username: User's username
        :param str password: User's password
        :param str confirm_password: User's confirmed password
        :param str email: User's email

        :returns: Account object instantiated with current user id

        :raises UsernameAlreadyExists: if username is already registered in the database
        :raises InvalidUsername: if username doesn't match the required pattern
        :raises PasswordDoNotMatch: if password and confirm_password are not the same
        :raises InvalidPassword: if password doesn't match the required pattern
        :raises EmailAlreadyExists: if email is already registered in the database
        :raises InvalidEmail: if email doesn't match the email pattern

        """
        try:
            cls.username_validator.unique(username)
        except ValidationFailure:
            raise UsernameAlreadyExists
        try:
            cls.username_validator.pattern(username)
        except ValidationFailure:
            raise InvalidUsername

        try:
            cls.password_validator.pattern(password)
        except ValidationFailure:
            raise InvalidPassword
        try:
            cls.password_validator.match(password, confirm_password)
        except ValidationFailure:
            raise PasswordsDoNotMatch

        try:
            cls.email_validator.unique(email)
        except ValidationFailure:
            raise EmailAlreadyExists
        try:
            cls.email_validator.pattern(email)
        except ValidationFailure:
            raise InvalidEmail

        with database.database_manager() as db:
            # not using f-string due to SQL injection
            sql = """INSERT INTO lightning_pass.credentials (username, password, email)
                          VALUES ({},{},{})""".format(
                "%s",
                "%s",
                "%s",
            )
            db.execute(sql, (username, credentials.hash_password(password), email))

        return cls(credentials.get_user_item(username, "username", "id"))

    @classmethod
    def login(cls, username: str, password: str) -> Account:
        """Secondary class constructor for log in.

        Stores old last login date and updates new last login date

        :param str username: User's username
        :param str password: User's password

        :returns: Account object instantiated with current user id

        :raises AccountDoesNotExist: if username wasn't found in the database
        :raises AccountDoesNotExist: if password doesn't match with the hashed password in the database

        """
        try:
            cls.username_validator.unique(username, should_exist=True)
            cls.password_validator.authenticate(
                password,
                credentials.get_user_item(
                    username,
                    "username",
                    "password",
                ),
            )
        except ValidationFailure:
            raise AccountDoesNotExist

        account = cls(credentials.get_user_item(username, "username", "id"))
        account.last_login_date = account._last_login_date
        account.update_last_login_date()
        return account

    def validate_password_data(self, data: PasswordData) -> None:
        """Validate given password data container.

        Used when validating master password or new account password.
        Both of these operations use the same data containers.

        :param data: The data container

        :raises AccountDoesNotExist: If the authetication fails
        :raises InvalidPassword: If the new password doesn't match the required pattern
            Uses the validator of the current account
        :raises PasswordsDoNotMatch: If the passwords do not match

        """
        try:
            self.password_validator.authenticate(
                data.confirm_previous,
                self.password,
            )
        except ValidationFailure:
            raise AccountDoesNotExist

        try:
            self.password_validator.pattern(data.new_password)
        except ValidationFailure:
            raise InvalidPassword

        try:
            self.password_validator.match(
                data.new_password,
                data.confirm_new,
            )
        except ValidationFailure:
            raise PasswordsDoNotMatch

    def get_value(self, result_column: str) -> str | bytes | datetime:
        """Simplify getting user values.

        :param str result_column: Column from which we're collecting the value

        :returns: the result value

        """
        return credentials.get_user_item(self.user_id, "id", result_column)

    def set_value(
        self,
        result: int | str | bytes | datetime,
        result_column: str,
    ) -> None:
        """Simplify setting user values.

        :param str result: Value which we're inserting
        :param str result_column: Column where to insert the value

        """
        credentials.set_user_item(self.user_id, "id", result, result_column)

    def update_date(self, column: str) -> None:
        """Update database TIMESTAMP column with CURRENT_TIMESTAMP().

        Used for last_login_date and last_vault_unlock_date.

        :param column: Which column to update

        """
        with database.database_manager() as db:
            # not using f-string due to SQL injection
            sql = """UPDATE lightning_pass.credentials
                        SET {} = CURRENT_TIMESTAMP()
                      WHERE id = {}""".format(
                column,
                "%s",
            )
            # expecting a sequence thus val has to be a tuple (created by the trailing comma)
            db.execute(sql, (self.user_id,))

    @property
    def user_id(self):
        """Return database ID of the current account."""
        return self._user_id

    @property
    def username(self) -> str:
        """Username property.

        :returns: user's username in database

        """
        return self.get_value("username")

    @username.setter
    def username(self, value: str) -> None:
        """Set new username.

        :param str value: New username

        :raises UsernameAlreadyExists: if username is already registered in the database
        :raises InvalidUsername: if username doesn't match the required pattern

        """
        try:
            self.username_validator.validate_pattern(value)
        except ValidationFailure:
            raise InvalidUsername
        try:
            self.username_validator.validate_unique(value)
        except ValidationFailure:
            raise UsernameAlreadyExists

        self.set_value(value, "username")

    @property
    def password(self) -> bytes:
        """Password property.

        :returns: user's password in database

        """
        return self.get_value("password")

    @password.setter
    def password(self, data: PasswordData) -> None:
        """Password setter.

        :param data: The data container with all the necessary details.

        """
        self.validate_password_data(data)
        self.set_value(
            credentials.hash_password(str(data.new_password)),
            "password",
        )

    def reset_password(self, password: str, confirm_password: str) -> None:
        """"""
        if not self.password_validator.pattern(password):
            raise InvalidPassword
        if not self.password_validator.match(password, confirm_password):
            raise PasswordsDoNotMatch

        self.set_value(credentials.hash_password(password), "password")

    @property
    def email(self) -> str:
        """Email property.

        :returns: user's email in database

        """
        return self.get_value("email")

    @email.setter
    def email(self, value: str) -> None:
        """Set new email.

        :param str value: New email

        :raises EmailAlreadyExists: if email is already registered in the database
        :raises InvalidEmail: if email doesn't match the email pattern

        """
        try:
            self.email_validator.pattern(value)
        except ValidationFailure:
            raise InvalidEmail
        try:
            self.email_validator.unique(value)
        except ValidationFailure:
            raise EmailAlreadyExists

        self.set_value(value, "email")

    @property
    def profile_picture(self) -> str:
        """Profile picture property.

        :returns: user's profile picture in database

        """
        return self.get_value("profile_picture")

    @profile_picture.setter
    def profile_picture(self, filename: str) -> None:
        """Set new profile picture.

        :param str filename: Filename of the new profile picture

        """
        self.set_value(filename, "profile_picture")

    @property
    def profile_picture_path(self) -> str:
        """Profile picture path property.

        :returns: path to user's profile picture

        """
        return str(credentials.get_profile_picture_path(self.profile_picture))

    @property
    def _last_login_date(self) -> datetime:
        """Last login date property.

        :returns: last time the current account was accessed

        """
        return self.get_value("last_login_date")

    def update_last_login_date(self) -> None:
        """Update last login date."""
        self.update_date("last_login_date")

    @functools.cached_property
    def register_date(self) -> datetime:
        """Last login date property.

        Lru caching the register date to avoid unnecessary database queries,
        (register_date needs to be collected only once, it is not possible to change it.)

        :returns: register date of current user

        """
        return self.get_value("register_date")

    @property
    def master_password(self) -> str:
        """Return current master password."""
        return self.get_value("master_password")

    @master_password.setter
    def master_password(self, data: PasswordData) -> None:
        """Set a new master password.

        :param data: The data container will all the needed information

        :raises AccountDoesNotExist: if the normal password is not correct
        :raises PasswordsDoNotMatch: if the master passwords do not match
        :raises InvalidPassword: if the master password doesn't meet the required pattern

        """
        self.validate_password_data(data)
        self.set_value(
            credentials.hash_password(data.new_password),
            "master_password",
        )

    @property
    def _last_vault_unlock_date(self) -> datetime:
        """Return last vault unlock timestamp."""
        return self.get_value("last_vault_unlock_date")

    def update_last_vault_unlock_date(self) -> None:
        """Update the last vault unlock date."""
        self.update_date("last_vault_unlock_date")

    @property
    def vault_pages(self) -> Generator[Vault, None, None]:
        """Yield registered vault pages tied to the current account."""
        with database.database_manager() as db:
            # not using f-string due to SQL injection
            sql = """SELECT *
                       FROM lightning_pass.vaults
                      WHERE user_id = {}""".format(
                "%s",
            )
            # expecting a sequence thus val has to be a tuple (created by the trailing comma)
            db.execute(sql, (self.user_id,))
            result = db.fetchall()

        # list slice first element -> database primary key
        yield from (Vault(*vault[1:]) for vault in result if vault)

    @property
    def vault_pages_int(self) -> int:
        """Return an integer with the amount of vault pages a user has registered."""
        return sum(1 for _ in self.vault_pages)
