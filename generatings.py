import random
import string
import secrets
from random import randint
from faker import Faker

fake = Faker()


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(randint(8, 15)))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


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
