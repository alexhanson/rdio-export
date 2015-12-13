import json
from ._base import get_base_rdio_client


class _RdioExportClient(object):
    def __init__(self, base_client):
        self.base_client = base_client

    # Method will be called as method(start, batch_size)
    def _batch_call(self, method, batch_size):
        start = 0

        while True:
            batch = method(start, batch_size)

            for item in batch:
                yield item

            if (len(batch) < batch_size):
                break
            else:
                start += batch_size

    def get_current_user_key(self):
        return self.base_client.call('currentUser')['key']

    def get_collection_albums(self, current_user_key, batch_size=100):
        def get_album_batch(start, batch_size):
            return self.base_client.call(
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

        for album in self._batch_call(get_album_batch, batch_size):
            yield album

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
            # 'artistKey',
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
            'artist',
            'album',
            'albumKey',
            # 'albumUrl',
            # 'artistKey',
            # 'artistUrl',
            # 'type',
            # 'length',
            'duration',
            'isExplicit',
            'isClean',
            'url',
            # 'baseIcon',
            'albumArtist',
            # 'albumArtistKey',
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

    def get_playlist_data(self, current_user_key, batch_size=10):
        fields = [{'field': '*', 'exclude': True}]
        fields += map(lambda f: {'field': f}, [
            'name',
            'length',
            # 'type',
            'url',
            # 'icon',
            # 'baseIcon',
            # 'owner',
            # 'ownerUrl',
            # 'ownerKey',
            # 'ownerIcon',
            'lastUpdated',
            # 'shortUrl',
            # 'embedUrl',
            'key',
            # 'dynamicIcon',

            # Extras

            'hasCustomArtwork',
            # 'canStream',
            'isPublished',
            # 'iframeUrl',
            # 'iconKeys',
            # 'customIconKey',
            # 'reasonNotViewable',
            'description',
            # 'radioKey',
            'dominantColor',
            # 'canTether',
            # 'icon400',
            # 'tracks',
            'trackKeys',
            'bigIcon1200',
            # 'isViewable',
            # 'bigIcon',
        ])

        def get_playlist_batch(start, batch_size):
            return self.base_client.call(
                'getUserPlaylists',
                user=current_user_key,
                sort='name',
                start=start,
                count=batch_size,
                extras=json.dumps(fields),
            )

        for playlist in self._batch_call(get_playlist_batch, batch_size):
            yield playlist


def get_rdio_client():
    base_client = get_base_rdio_client()
    return _RdioExportClient(base_client)
