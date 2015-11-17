import json
import os
from collections import namedtuple
from rdioapi import Rdio

_CONFIG_PATH = os.path.expanduser('~/.rdio-export.json')

_RdioConfig = namedtuple('RdioConfig', [
    'credentials',
    'client_state',
])

_RdioCredentials = namedtuple('RdioCredentials', [
    'client_id',
    'client_secret',
])


def _get_stored_config():
    credentials = {}
    client_state = {}

    if os.path.exists(_CONFIG_PATH):
        print u"Reading configuration from {}".format(_CONFIG_PATH)
        with open(_CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
            credentials = config.get('credentials', credentials)
            client_state = config.get('client_state', client_state)

    return _RdioConfig(
        credentials=credentials,
        client_state=client_state,
    )


def _add_missing_config(config):
    credentials = config.credentials

    client_id = credentials.get('client_id', None)
    if client_id is None:
        client_id = raw_input(u"Client ID: ")

    client_secret = credentials.get('client_secret', None)
    if client_secret is None:
        client_secret = raw_input(u"Client secret: ")

    new_credentials = _RdioCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )

    return _RdioConfig(
        credentials=new_credentials,
        client_state=config.client_state,
    )


def _set_stored_config(config):
    config_dict = {
        'credentials': {
            'client_id': config.credentials.client_id,
            'client_secret': config.credentials.client_secret,
        },
        'client_state': config.client_state,
    }

    with open(_CONFIG_PATH, 'w') as config_file:
        json.dump(config_dict, config_file, indent=4)


def get_base_rdio_client():
    config = _get_stored_config()
    config = _add_missing_config(config)
    needs_auth = len(config.client_state) == 0

    rdio = Rdio(
        config.credentials.client_id,
        config.credentials.client_secret,
        config.client_state
    )

    if needs_auth:
        rdio.begin_authentication()
        url, device_code = rdio.begin_authentication()
        print u"Please enter device code {} on {}".format(device_code, url)
        rdio.complete_authentication()

    _set_stored_config(config)
    return rdio
