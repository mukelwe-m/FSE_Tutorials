# Just check if the student has loaded the environment variables correctly
from helpers.config import Config

# Making a simple test to check if the environment variables are loaded correctly
def test_currency_symbol():
    assert Config.get_currency_symbol() == "R"


def test_secret_key():
    assert Config.get_secret_key() == "supersecretkey"
