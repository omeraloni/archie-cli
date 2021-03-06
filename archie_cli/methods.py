import json
import os
import logging
import subprocess

from hashlib import md5
from .archie import Archie


def archie_reboot(debug_mode=False):

    cfg = config_read()

    archie = Archie(host=cfg["host"], username=cfg["username"], password=cfg["password"], debug_mode=debug_mode)
    archie.login()
    archie.reboot()
    logging.getLogger('archie-cli').warning("Router is rebooting")


def archie_test_login(debug_mode=False):

    cfg = config_read()

    archie = Archie(host=cfg["host"], username=cfg["username"], password=cfg["password"], debug_mode=debug_mode)

    try:
        archie.login()
        logging.getLogger('archie-cli').info(f"Logged-in, token is {archie.token}")
    except ValueError as e:
        logging.getLogger('archie-cli').error(e)


def config_write(host, username, password):
    path = f"{os.environ.get('HOME')}/.config/archie"

    if os.path.exists(path) is False:
        os.mkdir(path)

    os.chdir(path)

    config_file = f"{path}/config.json"

    # get the absolute path of ping command to overcome cron environment issues
    output, err = subprocess.Popen(["which", "ping"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    ping_cmd = output.decode('utf-8').rstrip('\n')

    with open(config_file, 'w') as file:
        cfg = {
            'host': host,
            'username': username,
            'password': md5(password.encode('utf')).hexdigest(),
            'ping_cmd': ping_cmd
        }

        json.dump(cfg, file)
        print('Saved!')


def config_read():
    config_file = f"{os.environ.get('HOME')}/.config/archie/config.json"

    if os.path.isfile(config_file) is False:
        raise FileNotFoundError("Configuration file not found")

    with open(config_file, 'r') as file:
        return json.load(file)


def config_check_password(password):
    return md5(password.encode('utf')).hexdigest() == config_read()['password']