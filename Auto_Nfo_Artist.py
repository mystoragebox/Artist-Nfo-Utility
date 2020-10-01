import os
import time
import musicbrainzngs
# IMPORTANT!!!!!!!!!!!!!! input your own useragent below. 'name', 'version', 'website'
musicbrainzngs.set_useragent('', '', '')

# key: [key from server, opening tag, closing tag]
Tags = {
    'name': ('name', '\n  <title>', '</title>'),
    'id': ('id', '\n  <musicbrainzartistid>', '</musicbrainzartistid>'),
    'sortname': ('sort-name', '\n  <sortname>', '</sortname>'),
    'type': ('type', '\n  <type>', '</type>'),
    'gender': ('gender', '\n  <gender>', '</gender>'),
    'country': ('country', '\n  <country>', '</country>'),
    'begin': ('begin', '\n  <formed>', '</formed>', '\n  <born>', '</born>'),
    'end': ('end', '\n  <disbanded>', '</disbanded>', '\n  <died>', '</died>'),
    'tag-list': ('Acoustic', 'Alternative', 'Ambient', 'Blues', 'Children', 'Christian', 'Christmas', 'Classic', 'Classical', 'Club', 'Comedy', 'Contemporary', 'Country', 'Dance', 'Disco', 'Dubstep', 'Easy Listening', 'Electronic', 'Euro', 'Experimental', 'Folk', 'Funk', 'Garage', 'Gospel', 'Goth', 'Grunge', 'Hip Hop', 'House', 'Indie', 'Industrial', 'Instrumental', 'Jazz', 'Latin', 'Mash Up', 'Metal', 'Opera', 'Orchestral', 'Pirate', 'Pop','Progressive', 'Psych', 'Punk', 'R&B', 'Reggae', 'Rap', 'Rock', 'Ska', 'Soft', 'Soul', 'Soundtrack', 'Southern', 'Symphonic', 'Symphony', 'Techno', 'Trance', 'Trip Hop', 'Urban', 'Vocal'),
}

# variables. Change the base to the folder the artists are in.
base = 'MUSIC VIDEOS/'
noTags = len(Tags)
genres = []
Tagskeys = []
artistId = ['placeholder']
listNum = 1
folderList = []
folderError = []

for key in Tags:
    Tagskeys.append(key)

# get list of artist folders
for entry in os.listdir(base):
    if os.path.isdir(os.path.join(base, entry)):
        folderList.append(entry)

# Iterate over all folders
for folder in folderList:
    artistDir = base + folder + '/'

    # Skip files that already exist. Delete this if you want to overwrite old nfo files.
    if os.path.isfile(artistDir + 'artist.nfo'):
        continue

    # Start Search
    result = musicbrainzngs.search_artists(artist=folder)
    try:
        results = result['artist-list'][0]['id']
    except:
        folderError.append(folder)
        continue

    # get the artist information
    try:
        rsltChk = musicbrainzngs.get_artist_by_id(results, includes=['tags'])
    except WebServiceError as exc:
        folderError.append(folder)
        continue
    else:
        finalArtist = rsltChk

    # get tags from artist information
    if 'tag-list' in rsltChk['artist']:
        glist = rsltChk['artist']['tag-list']
        for x in glist:
            tagname = x['name']
            tagname = tagname.lower()
            genres.append(tagname)

    # build nfo file
    nfo = open(artistDir + 'artist.nfo', 'w', encoding='utf-8')
    nfo.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<artist>')

    for x in range(noTags):
        keys = Tagskeys[x]
        tags = Tags[keys]

        if (tags[0] == 'begin') or (tags[0] == 'end'):
            if 'life-span' in rsltChk['artist'] and tags[0] in rsltChk['artist']['life-span']:
                html = Tags[keys]
                i = rsltChk['artist']['life-span'][tags[0]]
                if rsltChk['artist']['type'] == 'Person':
                    nfo.write(html[3] + i + html[4])
                else:
                    nfo.write(html[1] + i + html[2])

        elif keys == 'tag-list' and 'tag-list' in rsltChk['artist']:
            for gen in Tags['tag-list']:
                gens = gen.lower()
                if gens in str(genres):
                    nfo.write('\n  <genre>' + gen + '</genre>')

        elif tags[0] in rsltChk['artist']:
            html = Tags[keys]
            i = rsltChk['artist'][tags[0]]
            nfo.write(html[1] + i + html[2])

    nfo.write('\n</artist>')
    nfo.close()

    # clear the data for next query
    artistId.clear()
    genres.clear()
    listNum = 1
    artistId.append('placeholder')
    print(folder + ' Completed')

    # Sleep. Required so your ip doesn't get blacklisted
    time.sleep(1.1)

# Report any errors
if not folderError:
    print('\nCompleted all folders. No errors to report')
else:
    print('\nCompleted with errors, please see these folders:')
    for i in folderError:
        print(i)
