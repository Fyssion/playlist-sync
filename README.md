# playlist-sync

Just a shitty and possibly over engineered Python script for syncing
playlists between music streaming services. Right now it only supports
syncing between Spotify and YTMusic because that's all I need.

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

You'll need to get your Spotify API credentials.
Visit the [Spotify developer dashboard][spotify-dashboard] to get them.

To sync from Spotify to YT Music, use the following command:

```sh
# Windows
py -m playlist_sync spotify-to-yt -f "<SPOTIFY_URL>" -t "<YT_ID>"

# MacOS/Linux
python3 -m playlist_sync spotify-to-yt -f "<SPOTIFY_URL>" -t "<YT_ID>"
```

Replace `<SPOTIFY_URL>` and `<YT_ID>` with the Spotify playlist URL
and YouTube playlist ID respectively.

To get the YouTube playlist ID, click the share button on the playlist
page in YouTube Music, and copy the ID after `list=`, as shown below:

```re
https://music.youtube.com/playlist?list=[THIS_PART_OF_THE_URL]&si=NOT_THIS
```

If you want to sync from YT Music to Spotify, modify the command above to look
like this:

```sh
(py -m | python3 -m) playlist_sync yt-to-spotify -f "<YT_ID>" -t "<SPOTIFY_URL>"
```

On the first run, it'll ask you to paste your browser credentials for
YouTube music. Instructions for finding the credentials can be found
in the [ytmusicapi documentation][ytmusicapi-browser].

It'll also ask you to perform some Spotify OAuth setup to authorize the
program with your Spotify account. Just follow the instructions in the
terminal.

After that, it'll start syncing. If you run into any issues, feel free to
open a discussion post and I can try to help.

### Config file

If you don't want to type your Spotify credentials into the CLI on every run,
you can create a `config.py` file. Here's an example of that:

```py
spotify_client_id = 'spotify client id'
spotify_client_secret = 'spotify client secret'
```

[ytmusicapi-browser]: https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#copy-authentication-headers
[spotify-dashboard]: https://developer.spotify.com/dashboard
