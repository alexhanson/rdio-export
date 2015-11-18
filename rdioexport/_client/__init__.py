import json
from ._base import get_base_rdio_client


class _RdioExportClient(object):
    def __init__(self, base_client):
        self.base_client = base_client

    def get_current_user_key(self):
        return self.base_client.call('currentUser')['key']

    def get_collection_albums(self, batch_size=100):
        current_user_key = self.get_current_user_key()
        start = 0

        while True:
            batch = self.base_client.call(
                'getAlbumsInCollection',
                user=current_user_key,
                sort='dateAdded',
                start=start,
                count=batch_size,
                extras=json.dumps([
                    {'field': '*', 'exclude': True},
                    {'field': 'albumKey'},
                    {'field': 'trackKeys'},
                ]),
            )

            for album in batch:
                yield album

            if (len(batch) < batch_size):
                break
            else:
                start += batch_size

    def get_album_data(self, album_keys):
        fields = [
            {'field': '*', 'exclude': True},
            {
                'field': 'label',
                'extras': [
                    {'field': '*', 'exclude': True},
                    {'field': 'key'},
                    {'field': 'name'},
                ],
            }
        ]
        fields += map(lambda f: {'field': f}, [
            'name',
            # 'type',
            # 'icon',
            # 'baseIcon',
            'url',
            'artist',
            # 'artistUrl',
            'isExplicit',
            'isClean',
            'length',
            'artistKey',
            'trackKeys',
            # 'price',
            # 'canStream',
            # 'canSample',
            # 'canTether',
            # 'shortUrl',
            # 'embedUrl',
            # 'displayDate',
            'key',
            # 'releaseDate',
            'duration',
            # 'dynamicIcon',

            # Extras

            # 'radioKey',
            'popularTracks',
            # 'artistAvatarIcon',
            # 'tracks',
            'isCompilation',
            # 'streamRegions',
            # 'hasListened',
            'dominantColor',
            # 'icon400',
            # 'backgroundImageUrl',
            # 'iframeUrl',
            'bigIcon1200',
            'releaseDateISO',
            'upcs',
            # 'bigIcon',
            # 'iconKey',
        ])

        return self.base_client.call(
            'get',
            keys=','.join(album_keys),
            extras=json.dumps(fields),
        )

    def get_track_data(self, track_keys):
        fields = [{'field': '*', 'exclude': True}]
        fields += map(lambda f: {'field': f}, [
            'name',
            # 'artist',
            'album',
            'albumKey',
            # 'albumUrl',
            'artistKey',
            # 'artistUrl',
            # 'type',
            # 'length',
            'duration',
            'isExplicit',
            'isClean',
            'url',
            # 'baseIcon',
            # 'albumArtist',
            'albumArtistKey',
            # 'canDownload',
            # 'canDownloadAlbumOnly',
            # 'canStream',
            # 'canTether',
            # 'canSample',
            # 'price',
            # 'shortUrl',
            # 'embedUrl',
            'key',
            # 'gridIcon',
            # 'icon',
            # 'icon400',
            'trackNum',
            # 'radioKey',
            # 'radio',
            # 'dynamicIcon',

            # Extras

            'isInCollection',
            # 'streamRegions',
            'isrcs',
            # 'backgroundImageUrl',
            # 'canTetherForRegion',
            # 'sampleUrl',
            # 'isOnCompilation',
            # 'artistAvatarIcon',
            'playCount',
            # 'iframeUrl',
            # 'bigIcon',
            # 'iconKey',
            # 'dominantColor',
            # 'tetherRegions',
        ])

        return self.base_client.call(
            'get',
            keys=','.join(track_keys),
            extras=json.dumps(fields),
        )


def get_rdio_client():
    base_client = get_base_rdio_client()
    return _RdioExportClient(base_client)
