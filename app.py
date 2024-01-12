from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, render_template, url_for
import requests
import urllib.parse
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotGraphs
import getTopUserData

load_dotenv()

clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
redirectURI = 'http://127.0.0.1:5000/callback'

authorizeURL = 'https://accounts.spotify.com/authorize'
tokenURL = 'https://accounts.spotify.com/api/token'
appScope = 'user-read-private user-read-email playlist-read-private playlist-read-collaborative user-top-read'


app = Flask(__name__)

@app.route('/')
def index():
    auth_params = {
        'client_id': clientId,
        'response_type': 'code',
        'redirect_uri': redirectURI,
        'scope': appScope
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(auth_params)
    return render_template("loginPage.html", auth_url=auth_url)
    
@app.route('/callback')
def displayOptions():
    setTokenAndId()
    return render_template("homePage.html")

def setTokenAndId():
    code = request.args.get('code')  # Get the authorization code from the redirect URL
    token_url = 'https://accounts.spotify.com/api/token'

    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirectURI,
        'client_id': clientId,
        'client_secret': clientSecret
    }

    # Exchange authorization code for access token
    token_response = requests.post(token_url, data=token_params)
    if token_response.status_code == 200:
        token_info = token_response.json()
        global access_token
        access_token = token_info['access_token']
        
        # Use the access token to fetch user information
        user_profile_url = 'https://api.spotify.com/v1/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        user_profile_response = requests.get(user_profile_url, headers=headers)
        if user_profile_response.status_code == 200:
            user_data = user_profile_response.json() 
            global userId 
            userId= user_data['id']

@app.route('/userInfo')
def displayUserInfo():
    top99TracksShortTerm, top99TracksMediumTerm, top99TracksLongTerm = getTopUserData.getTrackInfo(access_token)
    top99ArtistsShortTerm, shortTermGenres, top99ArtistsMediumTerm, mediumTermGenres, top99ArtistsLongTerm, longTermGenres = getTopUserData.getArtistInfo(access_token)

    
    top99TracksShortTerm, top99TracksMediumTerm, top99TracksLongTerm = top99TracksShortTerm.to_html(index=False, classes='table', escape=False, table_id='tracks-shortTerm'), top99TracksMediumTerm.to_html(index=False, classes='table', escape=False, table_id='tracks-mediumTerm'), top99TracksLongTerm.to_html(index=False, classes='table', escape=False, table_id='tracks-longTerm')
    top99ArtistsShortTerm, top99ArtistsMediumTerm, top99ArtistsLongTerm = top99ArtistsShortTerm.to_html(index=False, classes='table', escape=False, table_id='artists-shortTerm'), top99ArtistsMediumTerm.to_html(index=False, classes='table', escape=False, table_id='artists-mediumTerm'), top99ArtistsLongTerm.to_html(index=False, classes='table', escape=False, table_id='artists-longTerm')

    top99GenresShortTerm, top99GenresMediumTerm, top99GenresLongTerm = shortTermGenres.to_html(index=False, classes='table', escape=False, table_id='genres-shortTerm'), mediumTermGenres.to_html(index=False, classes='table', escape=False, table_id='genres-mediumTerm'), longTermGenres.to_html(index=False, classes='table', escape=False, table_id='genres-longTerm')

    return render_template("topSongsInfo.html", top99TracksShortTerm=top99TracksShortTerm, top99TracksMediumTerm=top99TracksMediumTerm, 
                           top99TracksLongTerm=top99TracksLongTerm, top99ArtistsShortTerm=top99ArtistsShortTerm, 
                           top99ArtistsMediumTerm=top99ArtistsMediumTerm, top99ArtistsLongTerm=top99ArtistsLongTerm, 
                           top99GenresShortTerm=top99GenresShortTerm, top99GenresMediumTerm=top99GenresMediumTerm, top99GenresLongTerm=top99GenresLongTerm)
    


    


@app.route('/playlistdata')
def displayPlaylistLinks():
    setTokenAndId()
    playlistNames, playlistIds, playlistImages = getPlaylistIds()
    size = len(playlistNames)
    # playlistData = zip(playlistNames, playlistIds, playlistImages)
   
    return render_template("displayPlaylists.html", playlistNames=playlistNames, playlistIds=playlistIds, playlistImages=playlistImages, 
                           size=size)
   # return render_template("displayPlaylists.html", playlistData=playlistData)

def getPlaylistIds(): # Returns lists of user's playlist names, ids, and images
    offset = 0
    playlist_names = []
    playlist_ids = []
    playlist_images = []
    while True:
        link = 'https://api.spotify.com/v1/users/' + userId + '/playlists?limit=50&offset=' + str(offset) 
        headers = {'Authorization': f'Bearer {access_token}'}

        playlistData = requests.get(link, headers=headers)
        playlistJson = playlistData.json()

        playlistArray = playlistJson['items']

        if playlistArray:
            for playlist in playlistArray:
                playlist_names.append(playlist['name'])
                playlist_ids.append(playlist['id'])

                if (playlist['images']):
                    playlist_images.append(playlist['images'][0]['url'])
                else:
                    playlist_images.append('https://i.imgur.com/2k42Dap.jpg')
                
        else:
            break
        offset += 50
    return playlist_names, playlist_ids, playlist_images

@app.route('/playlistdata/<playlistId>')
def plotAllGraphs(playlistId):
    testId = playlistId

    songInformation = getSongInformation(testId)

    artistFreqGraph = plotGraphs.plotArtistFrequencyGraph(songInformation)
    albumReleaseDatesGraph = plotGraphs.plotAlbumReleaseDates(songInformation)
    albumToArtistTreemap = plotGraphs.plotAlbumsToArtistsGraph(songInformation)
    radarGraph, songEnergyAvg, songDancibilityAvg, songInstrumentalnessAvg, songValenceAvg = plotGraphs.plotRadarChart(songInformation)
    tempoGraph, highestTempoTable, lowestTempoTable = plotGraphs.plotTempoData(songInformation)
    modeGraph = plotGraphs.plotModeGraph(songInformation)
    explicitWordsGraph = plotGraphs.plotExplicitChart(songInformation)
    popularityGraph, songLengthGraph = plotGraphs.plotSongBoxPlots(songInformation)

    return render_template(
        "renderGraphs.html", artistFreqGraph = artistFreqGraph, 
        albumReleaseDatesGraph = albumReleaseDatesGraph, radarGraph = radarGraph, songEnergyAvg = songEnergyAvg, 
        songDancibilityAvg = songDancibilityAvg, songInstrumentalnessAvg = songInstrumentalnessAvg, songValenceAvg = songValenceAvg,
        modeGraph=modeGraph, albumToArtistTreemap=albumToArtistTreemap, tempoGraph=tempoGraph, highestTempoTable=highestTempoTable,
        lowestTempoTable=lowestTempoTable, explicitWordsGraph=explicitWordsGraph, popularityGraph=popularityGraph, songLengthGraph=songLengthGraph)


def getSongInformation(playlistId): # Get a dataframe object with all needed data to create the statistics graphs
    offset = 0
    listOfSongIds = []
    listOfRows = []

    #df = pd.DataFrame(columns=['songName', 'songId', 'songLength', 'songTempo', 'songKey', 'songEnergy', 'songDancibility', 'songPopularity', 'artists', 'artistsId', 'albumName', 'albumReleaseDate'])
    while True:
       # link = 'https://api.spotify.com/v1/playlists/' + playlistId + '/tracks?fields=items%28track%28album%28name%2C+release_date%29%2Cartists%28name%2C+id%29%2C+duration_ms%2C+name%2C+id%2C+popularity%29%29&limit=50&offset=' + str(offset)
        link = 'https://api.spotify.com/v1/playlists/' + playlistId + '/tracks?fields=items%28track%28id%2C+artists%28name%2C+id%29%2Cname%2Cduration_ms%2Cexplicit%2Cpopularity%2Cpreview_url%2C+album%28album_type%2Cid%2Cname%2Crelease_date%2Cimages%28url%29%29%29%29&limit=50&offset=' + str(offset)
        offset += 50
        headers = {'Authorization': f'Bearer {access_token}'}
        trackDataRequest = requests.get(link, headers=headers)
        allTrackData = trackDataRequest.json()

        items = allTrackData["items"]

        if items:
            for item in items:
                
                track = item['track']

                songName = track['name']
                songId = track['id']
    
                songLength = float(track['duration_ms']) / 1000.0
                songPopularity = track['popularity']
                #  songImage = track['album']['images'][0]['url']
                isExplicit = track['explicit']
                #   previewUrl = track['preview_url']
                
                albumName = track['album']['name']
                albumRelease = track['album']['release_date']

                artists = []
                artistsIds = []
                
                for currentArtist in track['artists']:
                    artists.append(currentArtist['name'])
                    artistsIds.append(currentArtist['id'])
                
                listOfSongIds.append(songId)

                

                #  newRow = [songName, songId, songLength, songPopularity, songImage, isExplicit, previewUrl, artists, artistsIds, albumName, albumRelease]
                newRow = [songName, songId, songLength, songPopularity, isExplicit, artists, artistsIds, albumName, albumRelease]
                listOfRows.append(newRow)
                
        else:
            break

    df = pd.DataFrame(listOfRows, columns=['songName', 'songId', 'songLength', 'songPopularity', 'isExplicit', 'artists', 'artistsId', 'albumName', 'albumReleaseDate'])

    currentStart = 0
    batchSize = 100

    while currentStart < len(listOfSongIds):
        uniqueIds = ''
        currentEnd = min(currentStart + batchSize, len(listOfSongIds))

        for i in range(currentStart, currentEnd):
            uniqueIds += listOfSongIds[i] + ','
        uniqueIds = uniqueIds.rstrip(',')

        songLinks = 'https://api.spotify.com/v1/audio-features?ids=' + uniqueIds
        songDataRequest = requests.get(songLinks, headers=headers)
        songData = songDataRequest.json()

        for item in songData['audio_features']:
            songId = item['id']
            currentRow = 0

            songTempo = item['tempo']
            songKey = item['mode']
            songEnergy = item['energy']
            songDancibility = item['danceability']
            songInstrumentalness = item['instrumentalness']
            songValence = item['valence']
            
            currentRow = df[df['songId'] == songId].index[0]
           
            df.loc[currentRow, 'songTempo'] = songTempo
            df.loc[currentRow, 'songKey'] = songKey
            df.loc[currentRow, 'songEnergy'] = songEnergy
            df.loc[currentRow, 'songDancibility'] = songDancibility
            df.loc[currentRow, 'songInstrumentalness'] = songInstrumentalness
            df.loc[currentRow, 'songValence'] = songValence

            currentRow += 1

            
        currentStart += batchSize

    return df



    

    




 

if __name__ == '__main__':
    app.run(debug=True)