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

# empty variables
noTags = len(Tags)
genres = []
Tagskeys = []
artistId = ['placeholder']
listNum = 1
allArtist = []

for key in Tags:
    Tagskeys.append(key)

# while you want to input data
while True:
    # Start Search
    print('This loop will keep going until you type "end"\n')
    srch = input('Which artist would you like to search for? ')
    if srch == 'end':
        break
    
    result = musicbrainzngs.search_artists(artist=srch)
    try:
        results = result['artist-list'][0]['id']
    except:
        print('\nThat didn\'t match any artists on MusicBrainz. Please try again.\n')
        time.sleep(1)
        continue

    # Loop through and print results, append to artist id list
    for artist in result['artist-list']:
        artistId.append(artist['id'])
        print(str(listNum) + ': ' + artist['name'] + ' musicbrainz ID:' + artist['id'])
        listNum += 1

        # Limit amount of results
        if listNum == 6:
            break

    # user input to select best result
    print('\nChoose the correct artist from the list. If the same pick the first option.')
    UserInp = int(input('Input 1, 2 etc. '))
    UserChoice = artistId[UserInp]

    # get the artist information or break
    try:
        rsltChk = musicbrainzngs.get_artist_by_id(artistId[UserInp], includes=['tags'])
    except WebServiceError as exc:
        print('Something went wrong: %s' % exc)
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
    nfo = open('artist.nfo', 'w', encoding='utf-8')
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

    allArtist.append(srch)

    # clear the data for next query
    artistId.clear()
    genres.clear()
    listNum = 1
    artistId.append('placeholder')

    print(srch + ' nfo file completed sucessfully.\n')
    time.sleep(1)

print('\nDone. These are the artists you made files for:\n')
for i in allArtist:
    print(i)

