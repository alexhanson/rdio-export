import json
from ._base import get_base_rdio_client


class _RdioExportClient(object):
    def __init__(self, base_client):
        self.base_client = base_client

    def get_current_user_key(self):
        return self.base_client.call('currentUser')['key']

    def get_collection_by_album(self, batch_size=100):
        current_user_key = self.get_current_user_key()

        start = 0
        result = []

        while True:
            batch = self.base_client.call(
                'getAlbumsInCollection',
                user=current_user_key,
                sort='dateAdded',
                start=start,
                count=batch_size,
                extras=json.dumps([
                    {'field': '*', 'exclude': True},
                    {'field': 'key'},
                    {'field': 'trackKeys'},
                ]),
            )

            for album in batch:
                yield album

            if (len(batch) < batch_size):
                break
            else:
                start += batch_size

    def get_album_data(self, album_key):
        return self.base_client.call(
            'get',
            keys=album_key,
            extras=json.dumps([
                {'field': '*'},
                {
                    'field': 'track',
                    'extras': [
                        {'field': '*'},
                    ],
                },
            ]),
        )


def get_rdio_client():
    base_client = get_base_rdio_client()
    return _RdioExportClient(base_client)
