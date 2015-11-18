from ._client import get_rdio_client
from ._exporter import get_exporter
from itertools import chain, imap, islice


# Thanks to Roberto Bonvallet
# http://stackoverflow.com/a/1915307
def _split(iterable, batch_size):
    iterator = iter(iterable)
    batch = tuple(islice(iterator, batch_size))
    while batch:
        yield batch
        batch = tuple(islice(iterator, batch_size))


def archive_collection(
        rdio,
        exporter,
        album_batch_size=50,
        track_batch_size=200):
    collection_albums = rdio.get_collection_albums()

    album_count = 0
    track_count = 0

    for collection_album_batch in _split(collection_albums, album_batch_size):
        album_keys = map(lambda a: a['albumKey'], collection_album_batch)

        album_dict = rdio.get_album_data(album_keys)
        album_list = map(lambda k: album_dict[k], album_keys)
        exporter.write_albums(album_list)
        album_count += len(album_list)

        # We gather details about all tracks on an album -- even the ones that
        # aren't in our collection.
        track_keys_by_album = map(lambda a: a['trackKeys'], album_list)
        track_keys = chain.from_iterable(track_keys_by_album)

        for track_keys_batch in _split(track_keys, track_batch_size):
            track_dict = rdio.get_track_data(track_keys_batch)
            track_list = map(lambda k: track_dict[k], track_keys_batch)
            exporter.write_tracks(track_list)
            track_count += len(track_list)

        print u"Wrote {:,} albums and {:,} tracks so far. Still going...".format(
            album_count,
            track_count)

    print u"Wrote {:,} albums and {:,} tracks. Done!".format(
        album_count,
        track_count)
