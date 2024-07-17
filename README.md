# playlist-sync

Just a shitty and possibly over engineered Python script for syncing
playlists between music streaming services. Right now it only supports
syncing from Spotify to YTMusic because that's all I need.

This is only on GitHub because I spent multiple hours on this for no
reason. If it's actually helpful (or could be) and you want me to finish
it, open an issue and let me know.

## Installation

To install the project, assuming Python 3.11+ and Git are installed:

```sh
# Windows
py -m pip install git+https://github.com/Fyssion/playlist-sync.git

# MacOS/Linux
python3 -m pip install git+https://github.com/Fyssion/playlist-sync.git
```

## Usage

You'll need to create a `config.py` file. Here's an example of that:

```py
# Visit https://developer.spotify.com/dashboard to get your credentials
spotify_client_id = 'spotify client id'
spotify_client_secret = 'spotify client secret'

sync_from_url = 'url or id of spotify playlist to sync tracks from'
sync_to_id = 'id of youtube music playlist to sync tracks to (found in playlist URL)'
```

Then to run the program:

```sh
# Windows
py -m playlist_sync

# MacOS/Linux
python3 -m playlist_sync
```

On the first run, it'll ask you to paste your browser credentials for
YouTube music. Instructions for finding the credentials can be found
in the [ytmusicapi documentation][ytmusicapi-browser].

It'll also ask you to perform some Spotify OAuth setup to authorize the
program with your Spotify account. Just follow the instructions in the
terminal.

After that, it'll start syncing. If you run into any issues, feel free to
open a discussion post and I can try to help.

[ytmusicapi-browser]: https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#copy-authentication-headers
