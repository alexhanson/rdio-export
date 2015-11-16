from collections import namedtuple
from rdioapi import Rdio

RdioCredentials = namedtuple('RdioCredentials', [
	'client_id',
	'client_secret',
])

def get_credentials_from_input():
	client_id = raw_input("Client ID: ")
	client_secret = raw_input("Client secret: ")
	return RdioCredentials(
		client_id=client_id,
		client_secret=client_secret)

def get_rdio_client(credentials):
	state = {}
	return Rdio(
		credentials.client_id,
		credentials.client_secret,
		state)
