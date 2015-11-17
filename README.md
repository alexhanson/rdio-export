rdio-export
==============
Export Rdio collections and playlists in JSON format. **This tool is a work in progress, lacking in functionality and documentation.**

Since [Rdio is shutting down soon](http://press.pandora.com/phoenix.zhtml?c=251764&p=irol-newsArticle&ID=2112860), I also plan to make a tool to import Rdio collections and playlists into another streaming service. Since [Spotify has a public API](https://developer.spotify.com/), it's a strong contender.

# Using this tool
`rdio-export` is in active development, but here's how you can run the work-in-progress version:

## Setting up your Rdio app
`rdio-export` requires you use your own API access keys to make Rdio requests. Go to the [Create an app](https://www.rdio.com/developers/create/) page and populate the form. All fields are required, but `rdio-export` doesn't rely on any particular values.

* **App Name:** Anything you want.
* **Description:** Anything you want.
* **Developer Name:** Anything you want.
* **URL:** Anything you want — `http://localhost` works fine.
* **Redirect URIs:** Anything you want — `http://localhost` works fine.
* **Permissions:** Leave everything unchecked.
* **Platforms:** Since Python is cross-platform, I selected Windows, Mac, and Linux.

When finished, you should have a "Client ID" and "Client Secret" for your app. Keep note of these! You can always rediscover them by viewing [your Rdio apps](https://www.rdio.com/developers/your-apps/).

## Setting up your dev environment
1. Clone this repository and `cd` into it.
1. Using `pip` for Python 2.7, run `pip install -r bootstrap-requirements.txt`
1. Run `tox`

## Running `rdio-export`
From within this repository, run this command:

```
./dev/bin/rdio-export
```

On your first run, it will run you through an authentication procedure. After that, settings are kept in `~/.rdio-export.json`; if you experience issues, you can delete that file and try again.
