rdio-export
==============
Export Rdio collections and playlists in [newline-delimited JSON](http://ndjson.org/) format.

Galen Knapp is working on a [spotify-import](https://github.com/knappg/spotify-import) project that imports this data into Spotify.

# Using this tool
`rdio-export` requires a bit of setup. Here's how you do it:

## Setting up your Rdio app
`rdio-export` requires you use your own API access keys to make Rdio requests. Go to the [Create an app](https://www.rdio.com/developers/create/) page and populate the form. All fields are required, but `rdio-export` doesn't rely on any particular values.

* **App Name:** Anything you want.
* **Description:** Anything you want.
* **Developer Name:** Anything you want.
* **URL:** Anything you want — `http://localhost` works fine.
* **Redirect URIs:** Anything you want — `http://localhost` works fine.
* **Permissions:** Leave everything unchecked.
* **Platforms:** Since Python is cross-platform, I selected Windows, Mac, and Linux.

When finished, you should have a "Client ID" and "Client Secret" for your app. You'll need these values later, but you can always see them again by viewing [your Rdio apps](https://www.rdio.com/developers/your-apps/).

## Setting up your dev environment
1. Clone this repository and `cd` into it.
1. Using `pip` for Python 2.7, run `pip install -r requirements-bootstrap.txt`
1. Run `tox`

## Running `rdio-export`
From within this repository, run this command:

```
./dev/bin/rdio-export
```

On your first run, the program will guide you through an authentication procedure. After that, settings are kept in `~/.rdio-export.json`; if you experience issues, you can delete that file and try again.
