import json


class _RdioExporter(object):
    def __init__(self, album_filename, track_filename):
        self.album_file = open(album_filename, 'w')
        self.track_file = open(track_filename, 'w')

    def __del__(self):
        self.album_file.close()
        self.track_file.close()

    def write_albums(self, albums):
        for album in albums:
            json.dump(album, self.album_file)
            self.album_file.write('\n')
            self.album_file.flush()

    def write_tracks(self, tracks):
        for track in tracks:
            json.dump(track, self.track_file)
            self.track_file.write('\n')
            self.track_file.flush()


def get_exporter(album_filename, track_filename):
    return _RdioExporter(album_filename, track_filename)
