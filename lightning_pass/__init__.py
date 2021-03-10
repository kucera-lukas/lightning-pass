"""init"""
import pathlib

from .util import utils


def _copy(self: "pathlib.Path", target: "pathlib.Path") -> None:
    """Monkey Patch copy functionality into pathlib.Path object."""
    import shutil

    assert self.is_file()
    shutil.copy(str(self), str(target))  # str() only there for Python --version < 3.6


pathlib.Path.copy = _copy  # type: ignore

with utils.database_manager() as db:
    sql = """CREATE TABLE if not exists credentials(
            `id` int NOT NULL AUTO_INCREMENT,
            `username` varchar(255) NOT NULL,
            `password` varchar(255) NOT NULL,
            `email` varchar(255) NOT NULL,
            `profile_picture` varchar(255) NOT NULL DEFAULT 'default.png',
            `last_login_date` timestamp NULL DEFAULT NULL,
            `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
             PRIMARY KEY(`id`)
             )
             ENGINE = InnoDB
             AUTO_INCREMENT = 1
             DEFAULT CHARSET = utf8mb4
             COLLATE = utf8mb4_0900_ai_ci
             """
    db.execute(sql)
