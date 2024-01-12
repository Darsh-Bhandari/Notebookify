import requests
import pandas as pd

def getTrackInfo(access_token):
    ### SHORT TERM
    offset = 0
    listOfRows = []

    while True:
        link = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        trackData = requests.get(link, headers=headers)
        trackJson = trackData.json()

        trackArray = trackJson['items']

        if not trackArray:
            break

        for track in trackArray:
            songName = track['name']
            songPopularity = track['popularity']
            songAlbum = track['album']['name']
            songRelease = track['album']['release_date']
            songArtist = track['artists'][0]['name']

            songRelease = songRelease[0:4]
            
            listOfRows.append([songName, songArtist, songAlbum, songPopularity, songRelease])

        offset += 49

    top99TracksShortTerm = pd.DataFrame(listOfRows, columns=["Song Name", "Song Artist", "Song Album", "Song Popularity", "Song Release"])
    top99TracksShortTerm.insert(0, 'Rank', range(1, len(top99TracksShortTerm) + 1))

    ### MIDDLE TERM
    offset = 0
    listOfRows = []

    while True:
        link = 'https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        trackData = requests.get(link, headers=headers)
        trackJson = trackData.json()

        trackArray = trackJson['items']

        if not trackArray:
            break

        for track in trackArray:
            songName = track['name']
            songPopularity = track['popularity']
            songAlbum = track['album']['name']
            songRelease = track['album']['release_date']
            songArtist = track['artists'][0]['name']

            songRelease = songRelease[0:4]
            
            listOfRows.append([songName, songArtist, songAlbum, songPopularity, songRelease])

        offset += 49

    top99TracksMediumTerm = pd.DataFrame(listOfRows, columns=["Song Name", "Song Artist", "Song Album", "Song Popularity", "Song Release"])
    top99TracksMediumTerm.insert(0, 'Rank', range(1, len(top99TracksMediumTerm) + 1))

    ### LONG TERM
    offset = 0
    listOfRows = []

    while True:
        link = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        trackData = requests.get(link, headers=headers)
        trackJson = trackData.json()

        trackArray = trackJson['items']

        if not trackArray:
            break

        for track in trackArray:
            songName = track['name']
            songPopularity = track['popularity']
            songAlbum = track['album']['name']
            songRelease = track['album']['release_date']
            songArtist = track['artists'][0]['name']

            songRelease = songRelease[0:4]
            
            listOfRows.append([songName, songArtist, songAlbum, songPopularity, songRelease])

        offset += 49

    top99TracksLongTerm = pd.DataFrame(listOfRows, columns=["Song Name", "Song Artist", "Song Album", "Song Popularity", "Song Release"])
    top99TracksLongTerm.insert(0, 'Rank', range(1, len(top99TracksLongTerm) + 1))

    return top99TracksShortTerm, top99TracksMediumTerm, top99TracksLongTerm

def getArtistInfo(access_token):
    ### SHORT TERM
    offset = 0
    listOfRows = []
    shortTermGenreMap = {}
    totalGenres = 0

    while True:
        link = 'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        artistData = requests.get(link, headers=headers)
        artistJson = artistData.json()

        artistArray = artistJson['items']

        if not artistArray:
            break

        for artist in artistArray:
            listOfGenres = artist["genres"]
            artistName = artist['name']
            artistPopularity = artist['popularity']

            for genre in listOfGenres:
                totalGenres += 1
                if shortTermGenreMap.get(genre):
                    shortTermGenreMap[genre] += 1
                else:
                    shortTermGenreMap[genre] = 1

            stringOfGenres = ''
            if listOfGenres:
                stringOfGenres = ', '.join(listOfGenres)
                stringOfGenres.lstrip(', ')
                stringOfGenres.rstrip(', ')
            else:
                stringOfGenres = 'N/A'
            
            listOfRows.append([artistName, artistPopularity, stringOfGenres])

        offset += 49

    top99ArtistsShortTerm = pd.DataFrame(listOfRows, columns=["Name", "Popularity", "Genres"])
    top99ArtistsShortTerm.insert(0, 'Rank', range(1, len(top99ArtistsShortTerm) + 1))

    genreRowToAdd = []
    for genre, amount in shortTermGenreMap.items():
        percentage = (amount / totalGenres) * 100
        percentage = round(percentage, 2)
        genreRowToAdd.append([genre, percentage])
    
    shortTermGenreMapDf = pd.DataFrame(genreRowToAdd, columns=["Genre", "Percentage"])
    shortTermGenreMapDf = shortTermGenreMapDf.sort_values(by='Percentage', ascending=False)
    shortTermGenreMapDf.insert(0, 'Rank', range(1, len(shortTermGenreMapDf) + 1))
    

    ### MEDIUM TERM
    offset = 0
    listOfRows = []
    mediumTermGenreMap = {}
    totalGenres = 0

    while True:
        link = 'https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        artistData = requests.get(link, headers=headers)
        artistJson = artistData.json()

        artistArray = artistJson['items']

        if not artistArray:
            break

        for artist in artistArray:
            listOfGenres = artist["genres"]
            artistName = artist['name']
            artistPopularity = artist['popularity']

            for genre in listOfGenres:
                totalGenres += 1
                if mediumTermGenreMap.get(genre):
                    mediumTermGenreMap[genre] += 1
                else:
                    mediumTermGenreMap[genre] = 1

            stringOfGenres = ''
            if listOfGenres:
                stringOfGenres = ', '.join(listOfGenres)
                stringOfGenres.lstrip(', ')
                stringOfGenres.rstrip(', ')
            else:
                stringOfGenres = 'N/A'
            
            listOfRows.append([artistName, artistPopularity, stringOfGenres])

        offset += 49

    top99ArtistsMediumTerm = pd.DataFrame(listOfRows, columns=["Name", "Popularity", "Genres"])
    top99ArtistsMediumTerm.insert(0, 'Rank', range(1, len(top99ArtistsMediumTerm) + 1))
    
    genreRowToAdd = []
    for genre, amount in mediumTermGenreMap.items():
        percentage = (amount / totalGenres) * 100
        percentage = round(percentage, 2)    
        genreRowToAdd.append([genre, percentage])
    
    mediumTermGenreMapDf = pd.DataFrame(genreRowToAdd, columns=["Genre", "Percentage"])
    mediumTermGenreMapDf = mediumTermGenreMapDf.sort_values(by='Percentage', ascending=False)
    mediumTermGenreMapDf.insert(0, 'Rank', range(1, len(mediumTermGenreMapDf) + 1))

    ### LONG TERM
    offset = 0
    listOfRows = []
    longTermGenreMap = {}
    totalGenres = 0

    while True:
        link = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=49&offset=' + str(offset)
        headers = {'Authorization': f'Bearer {access_token}'}

        artistData = requests.get(link, headers=headers)
        artistJson = artistData.json()

        artistArray = artistJson['items']

        if not artistArray:
            break

        for artist in artistArray:
            listOfGenres = artist["genres"]
            artistName = artist['name']
            artistPopularity = artist['popularity']

            for genre in listOfGenres:
                totalGenres += 1
                if longTermGenreMap.get(genre):
                    longTermGenreMap[genre] += 1
                else:
                    longTermGenreMap[genre] = 1
            
            stringOfGenres = ''
            if listOfGenres:
                stringOfGenres = ', '.join(listOfGenres)
                stringOfGenres.lstrip(', ')
                stringOfGenres.rstrip(', ')
            else:
                stringOfGenres = 'N/A'
            
            listOfRows.append([artistName, artistPopularity, stringOfGenres])

        offset += 49

    top99ArtistsLongTerm = pd.DataFrame(listOfRows, columns=["Name", "Popularity", "Genres"])
    top99ArtistsLongTerm.insert(0, 'Rank', range(1, len(top99ArtistsLongTerm) + 1))
    
    genreRowToAdd = []
    for genre, amount in longTermGenreMap.items():
        percentage = (amount / totalGenres) * 100
        percentage = round(percentage, 2)
        genreRowToAdd.append([genre, percentage])
    
    longTermGenreMapDf = pd.DataFrame(genreRowToAdd, columns=["Genre", "Percentage"])
    longTermGenreMapDf = longTermGenreMapDf.sort_values(by='Percentage', ascending=False)
    longTermGenreMapDf.insert(0, 'Rank', range(1, len(longTermGenreMapDf) + 1))

    return top99ArtistsShortTerm, shortTermGenreMapDf, top99ArtistsMediumTerm, mediumTermGenreMapDf, top99ArtistsLongTerm, longTermGenreMapDf

    


    