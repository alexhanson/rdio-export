import os
import json


class _RdioExporter(object):
    def __init__(self, album_filename, track_filename, playlist_filename):
        self.album_file = self._open_file(album_filename)
        self.track_file = self._open_file(track_filename)
        self.playlist_file = self._open_file(playlist_filename)

        self.album_keys = set()
        self.track_keys = set()
        self.playlist_keys = set()

    def __del__(self):
        self.album_file.close()
        self.track_file.close()

    def _open_file(self, filename):
        if os.path.exists(filename):
            raise EnvironmentError("{} already exists".format(filename))
        else:
            return open(filename, 'w')

    def _print_stats(self):
        print u"Stats: {: >8,} albums {: >8,} tracks {: >8,} playlists".format(
            len(self.album_keys),
            len(self.track_keys),
            len(self.playlist_keys))

    def write_albums(self, albums):
        for album in albums:
            key = album['key']
            if key not in self.album_keys:
                json.dump(album, self.album_file)
                self.album_file.write('\n')
                self.album_file.flush()
                self.album_keys.add(key)

        self._print_stats()

    def write_tracks(self, tracks):
        for track in tracks:
            key = track['key']
            if key not in self.track_keys:
                json.dump(track, self.track_file)
                self.track_file.write('\n')
                self.track_file.flush()
                self.track_keys.add(key)

        self._print_stats()

    def write_playlists(self, playlists):
        for playlist in playlists:
            key = playlist['key']
            if key not in self.playlist_keys:
                json.dump(playlist, self.playlist_file)
                self.playlist_file.write('\n')
                self.playlist_file.flush()
                self.playlist_keys.add(key)

        self._print_stats()


def get_exporter(album_filename, track_filename, playlist_filename):
    return _RdioExporter(album_filename, track_filename, playlist_filename)
