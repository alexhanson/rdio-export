from ._client import get_rdio_client
from ._exporter import get_exporter
from itertools import chain, imap, islice
from operator import itemgetter


# Thanks to Roberto Bonvallet
# http://stackoverflow.com/a/1915307
def _split(iterable, batch_size):
    iterator = iter(iterable)
    batch = tuple(islice(iterator, batch_size))
    while batch:
        yield batch
        batch = tuple(islice(iterator, batch_size))


def _uniq(iterable):
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


def _write_tracks(rdio, exporter, track_keys_batch):
    track_dict = rdio.get_track_data(track_keys_batch)
    track_list = map(lambda k: track_dict[k], track_keys_batch)
    exporter.write_tracks(track_list)


def archive_collection(
        rdio,
        exporter,
        album_batch_size=50,
        track_batch_size=100):
    print u"\nStarting to archive collection..."

    current_user_key = rdio.get_current_user_key()
    collection_albums = rdio.get_collection_albums(current_user_key)

    for collection_album_batch in _split(collection_albums, album_batch_size):
        album_keys = map(lambda a: a['albumKey'], collection_album_batch)

        album_dict = rdio.get_album_data(album_keys)
        album_list = map(lambda k: album_dict[k], album_keys)
        exporter.write_albums(album_list)

        # We gather details about all tracks on an album -- even the ones that
        # aren't in our collection.
        track_keys_by_album = map(lambda a: a['trackKeys'], album_list)
        track_keys = chain.from_iterable(track_keys_by_album)

        for track_keys_batch in _split(track_keys, track_batch_size):
            num_written = _write_tracks(rdio, exporter, track_keys_batch)

    print u"Done writing collection!"


def archive_playlists(
        rdio,
        exporter,
        playlist_batch_size=10,
        track_batch_size=100):
    print u"\nStarting to archive playlists..."

    current_user_key = rdio.get_current_user_key()
    playlists = rdio.get_playlist_data(
        current_user_key,
        batch_size=playlist_batch_size)

    for playlist_batch in _split(playlists, playlist_batch_size):
        exporter.write_playlists(playlist_batch)

        track_keys_lists = map(lambda a: a['trackKeys'], playlist_batch)
        track_keys = _uniq(chain.from_iterable(track_keys_lists))

        for track_keys_batch in _split(track_keys, track_batch_size):
            num_written = _write_tracks(rdio, exporter, track_keys_batch)

    print u"Done writing playlists!"
