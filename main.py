from typing import Iterator, Protocol, TypeAlias
import sys
import logging
from generatings import generate_login, generate_password

log = logging.getLogger()
log.level = logging.DEBUG
log.addHandler(logging.StreamHandler(sys.stderr))

T_LOGIN: TypeAlias = str
T_PASSWORD: TypeAlias = str


class UserProtocol(Protocol):
    login: T_LOGIN
    password: T_PASSWORD


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password


def validate(users: list[UserProtocol], amount: int) -> None:
    logins = set(map(lambda user: user.login, users))
    if amount != (amount_of_logins := len(logins)):
        raise ValueError(
            f'Not enough of unique items. Required: "{amount}". Provided: "{amount_of_logins}"'
        )


def generate_users(amount: int) -> Iterator[UserProtocol]:
    logins: set[str] = set()
    passwords: set[str] = set()
    while len(logins) < amount or len(passwords) < amount:
        logins.add(generate_login())
        passwords.add(generate_password())
        log.info(f'Length login set {len(logins)}    Length password set {len(passwords)}')
    for _ in range(amount):
        user = User(logins.pop(), passwords.pop())
        yield user


def main():
    amount = 100_000
    users = list(generate_users(amount=amount))
    validate(users=users, amount=amount)


if __name__ == "__main__":
    main()
