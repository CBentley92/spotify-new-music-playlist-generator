# Spotify New Music Playlist Generator
Allows a playlist to be created via the Spotify api containing genuinely new music.\
The idea behind this started due to Spotify being terrible at suggesting good new music, usually favouring music it knows will be popular and generate them more listens.\
Therefore I want to make a script that can parse review sites, gather the well reviewed latest albums, and make a spotify playlist out of them.

# Current features
- Only generates new "Metal" genre playlists from metal-temple.com.
- Allows user to specify dates, minimum review score and number of tracks per album to include via "make_custom_playlist.py".
- Allows user to simply generate a playlist of well received albums from the last 2 weeks via "make_latest_playlist.py".

# Planned features
- Main goal is to generalise to other genres.
- Would like to allow user to enter a review website or custom list to generate the playlist.
- Need to build general review site parser.

# Install
- To check required packages are intalled run "install_required_packages.py".
- User must create a .env file in the directory with their spotify api credentials.
- Instructions to get api credentials here: https://developer.spotify.com/documentation/web-api/concepts/authorization.

# General Use
- If you just want the latest well received metal albums to sample, run "make_latest_playlist.py".
- If you want to specify the date range, minimum album rating and songs per album to include, run the "make_custom_playlist.py" with required arguments.
- Album reviews can be found within accompanying album list json file
