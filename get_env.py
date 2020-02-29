import os
from os.path import join, dirname
from dotenv import load_dotenv


def get_env(variable_name):
    load_dotenv(verbose=True)

    env_path = join(dirname(__file__), '.env')
    load_dotenv(env_path)

    return os.environ.get(variable_name)


if __name__ == "__main__":
    pass

    print(get_env("TEST"))
