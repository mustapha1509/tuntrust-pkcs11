import configparser
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


base_dir = get_base_dir()
config_file_path = os.path.join(base_dir, "config.ini")

config = configparser.ConfigParser()
config.read(config_file_path)

LIBRARY_PATH = config.get("PKCS11", "LIBRARY_PATH")
USER_PIN = config.get("PKCS11", "USER_PIN")
