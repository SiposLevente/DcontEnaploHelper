import configparser
import cryptography


def set_username(username):
    config = read_config("config.cfg")
    config.set("login-data", "username", username)
    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def set_password(password):
    config = read_config("config.cfg")
    config.set("login-data", "password",
               cryptography.encrypt_password(password))
    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def set_login_status(login_status):
    config = read_config("config.cfg")
    config.set("login-data", "logged-in", login_status)
    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def get_username():
    config = read_config("config.cfg")
    return config.get("login-data", "username")


def get_password():
    config = read_config("config.cfg")
    return cryptography.decrypt_password(config.get("login-data", "password"))


def get_login_status():
    config = read_config("config.cfg")
    return config.get("login-data", "logged-in")


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read("config.cfg")
    return config

