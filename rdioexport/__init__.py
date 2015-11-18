from ._client import get_rdio_client
from itertools import chain, imap, islice


# Thanks to Roberto Bonvallet
# http://stackoverflow.com/a/1915307
def _split(iterable, batch_size):
    iterator = iter(iterable)
    batch = tuple(islice(iterator, batch_size))
    while batch:
        yield batch
        batch = tuple(islice(iterator, batch_size))


def archive_collection(rdio, album_batch_size=50, track_batch_size=200):
    albums = rdio.get_collection_by_album()

    for album_batch in _split(albums, album_batch_size):
        album_keys = imap(lambda a: a['key'], album_batch)

        track_keys_by_album = imap(lambda a: a['trackKeys'], album_batch)
        track_keys = chain.from_iterable(track_keys_by_album)

        album_details = rdio.get_album_data(album_keys).values()
        print "Fetched {} albums".format(len(album_details))

        for track_keys_batch in _split(track_keys, track_batch_size):
            track_details = rdio.get_track_data(track_keys_batch).values()
            print "Fetched {} tracks".format(len(track_details))
