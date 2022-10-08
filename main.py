import random
from typing import Iterator, Protocol, TypeAlias
import string
import secrets
from random import randint
from faker import Faker
import sys
import logging

log = logging.getLogger()
log.level = logging.DEBUG
log.addHandler(logging.StreamHandler(sys.stderr))

fake = Faker()

T_LOGIN: TypeAlias = str
T_PASSWORD: TypeAlias = str


class UserProtocol(Protocol):
    login: T_LOGIN
    password: T_PASSWORD


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(randint(8, 15)))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def validate(users: list[UserProtocol], amount: int) -> None:
    logins = set(map(lambda user: user.login, users))
    if amount != (amount_of_logins := len(logins)):
        raise ValueError(
            f'Not enough of unique items. Required: "{amount}". Provided: "{amount_of_logins}"'
        )


def generate_login() -> str:
    fake_name = fake.name().split()
    additional_part = [secrets.randbelow(1000), random.randint(1950, 2022), f'{secrets.choice(string.ascii_letters)}',
                       f'{secrets.choice(string.ascii_letters)}{secrets.choice(string.ascii_letters)}']
    name_1 = [fake_name[0], fake_name[1]]
    name_2 = [fake_name[0], fake_name[1], '']
    username = fake.profile()['username']
    separator = ['_', '__', '.', '']

    main_part = [username, f'{secrets.choice(name_1)}{secrets.choice(separator)}{secrets.choice(name_2)}']
    return f'{secrets.choice(main_part)}{secrets.choice(separator)}{secrets.choice(additional_part)}'


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
