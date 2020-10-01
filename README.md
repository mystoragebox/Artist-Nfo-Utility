# Artist Nfo Utility
 If you have any use for artist info with your music or music videos this is for you. This utility has two scripts. `Nfo_Artist.py` lets you manually input artists to create the files and `Auto_Nfo_Artist.py` iterate through folders of artists. This is a solution to a very nich problem. Jellyfin is very limited for music videos and I had many music videos organised into artist folders. Because of this spending time making this script was quicker than manually making every nfo file.
## What Does It Do?
 These scripts will pull artist information from the MusicBrainz database and organise into an nfo file for easy reading with your prefered software. 
## Clean Up Genres
 While I made this utility I found there was many variations of genres like `Hip-Hop` and `Hip Hop` or `Rock` and `rock` To clean this up I made an editable tuple that has my prefered genres. Find `tag-list` in the `Tags` dictionary to add or delete genres.
## How To Run The Files
 You need to have Python, pip and musicbrainzngs installed. You also need to make a useragent for musicbrainzngs on line 5. The first variable is whatever you like, second is the version (1.0) and third is your website, github, reddit, facebook, whatever.
### How To Use Nfo_Artist.py
 1. Open cmd in the same folder as the script and type `py Nfo_Artist.py`
 1. It will prompt you for an artist name. Input and press enter.
 1. Pick the right artist by typing 1-5 and press enter.
 1. You will see artist.nfo file in the same folder as the script. Move this to your artist folder.
 1. Repeat from point 2.
 1. When you're done type `end`
### How To Use Auto_Nfo_Artist.py
 1. Copy the `Auto_Nfo_Artist.py` into the parent directory. For example:
  ```
  Parent
  __Music
  ____2Pac
  ____3 Doors Down
  ____etc...
  __Auto_Nfo_Artist.py
  ```
 1. Input the name of your music folder where that artist folders are: `base = 'MUSIC VIDEOS/'`
 1. Open cmd in the parent folder and type `py Auto_Nfo_Artist.py`
 1. It will iterate over all artist folders until it's finished. It will show any folders that had errors.
