import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import math

def plotArtistFrequencyGraph(df): # Return the html for the bar graph for artist frequency data in playlist
    artistsDict = {}

    col = df.loc[:, "artists"]

    for artists in col:
        for artist in artists:
            if artistsDict.get(artist):
                artistsDict[artist] += 1
            else:
                artistsDict[artist] = 1

    data2 = pd.DataFrame(artistsDict.items(), columns=['Artist', 'Frequency'])
    
    figure = px.bar(data2, x='Artist', y='Frequency', title='Artist Frequency')
    figure.update_layout(
        xaxis={'categoryorder': 'total descending', 'tickmode': 'linear'},
        yaxis={'title': 'Frequency', 'range': [0, max(data2['Frequency']) + 5]},
        autosize=True, 
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)
    )
    figure.update_traces(marker_color='#4C7F3A')

    graph_html_string = pio.to_html(figure, full_html=True)
    return graph_html_string

def plotAlbumReleaseDates(df): # Return the html for the bar graph for album release dates in playlist
    albumYears = {}

    dates = df.loc[:, "albumReleaseDate"]
    dates = dates.sort_values()

    for date in dates:
        year = int(date[0:4])
        if albumYears.get(year):
            albumYears[year] += 1
        else:
            albumYears[year] = 1

    chartData = pd.DataFrame(albumYears.items(), columns=['Year', 'Song Frequency'])

    figure = px.bar(chartData, x='Year', y='Song Frequency', title='Track Release Years')
    figure.update_layout(
        xaxis={'tickmode': 'linear'},
        yaxis={'title': 'Frequency'},
        plot_bgcolor='ghostwhite', 
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)  
    )
    figure.update_traces(marker_color='#4C7F3A')

    graph_html_string = pio.to_html(figure, full_html=False)
    return graph_html_string

def plotAlbumsToArtistsGraph(df): # Return the html to the album to artist treemap
    data = []
    seen_combinations = set()

    for _, row in df.iterrows():
        main_artist = row['artists'][0]
        album = row['albumName'] or 'No Album Title'
        song = row['songName']

        artist_album_combination = (main_artist, album)
        if artist_album_combination in seen_combinations:
            for entry in data:
                if entry['Artist'] == main_artist and entry['Album'] == album:
                    entry['Tracks'].append(song)
                    break
        else:
            seen_combinations.add(artist_album_combination)
            data.append({'Artist': main_artist, 'Album': album, 'Tracks': [song]})

    chartData = pd.DataFrame(data, columns=['Artist', 'Album', 'Tracks'])

    chartData['Track Total'] = chartData['Tracks'].apply(len)
    chartData['NumTracks'] = chartData['Tracks'].apply(len)
    chartData['Tracks'] = chartData['Tracks'].apply(lambda x: ', '.join(x))

    chartData = chartData.merge(chartData.groupby('Artist')['Track Total'].sum().reset_index(), how='left', left_on='Artist', right_on='Artist', suffixes=('_1', ''))


    figure = px.treemap(
        chartData,
        path=['Artist', 'Album'],
        values='NumTracks', 
        color='Track Total',
        hover_data={'Tracks': True, 'Track Total': True},  
        custom_data=['Tracks', 'Track Total', 'Artist', 'Album', 'NumTracks'], 
        title='Artist - Album - Track Count TreeMap', 
        color_continuous_scale='Sunset', 
        range_color=[1, chartData['Track Total'].max()]
    )
    
    figure.update_traces(  
        hovertemplate='<b>Album:</b> %{customdata[3]}<br><b>Artist:</b> %{customdata[2]}<br><b>Tracks:</b> %{customdata[0]}<br><b>Track Count:</b> %{customdata[4]}'
    ) 

    figure.update_layout(
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)  
    )

    graph_html_string = pio.to_html(figure, full_html=False)
    return graph_html_string


def plotRadarChart(df): # Return the html for the radar graph for random statistics in playlist
    songEnergyList = df.loc[:, 'songEnergy']
    songDancibilityList = df.loc[:, 'songDancibility']
    songInstrumentalnessList = df.loc[:, 'songInstrumentalness']
    songValenceList = df.loc[:, 'songValence']

    songEnergyAvg = 0
    songDancibilityAvg = 0
    songInstrumentalnessAvg = 0
    songValenceAvg = 0

    for i in range(0, len(songEnergyList)):
        songEnergyAvg += songEnergyList[i]
        songDancibilityAvg += songDancibilityList[i]
        songInstrumentalnessAvg += songInstrumentalnessList[i]
        songValenceAvg += songValenceList[i]

    songEnergyAvg = songEnergyAvg / len(songEnergyList)
    songDancibilityAvg = songDancibilityAvg / len(songDancibilityList)
    songInstrumentalnessAvg = songInstrumentalnessAvg / len(songInstrumentalnessList)
    songValenceAvg = songValenceAvg / len(songValenceList)

    data = pd.DataFrame(dict(
        r=[songEnergyAvg, songDancibilityAvg, songInstrumentalnessAvg, songValenceAvg],
        theta=['Track Energy','Track Dancibility','Track Instrumentalness',
            'Track Valence']))

    averages = []

    for i in range(0, 3):
        averages.append(data['theta'][i] + ": " + str(data['r'][i]))

    figure = px.line_polar(data, r='r', theta='theta', line_close=True, range_r=[0,1], title='Miscellanous Data')
    figure.update_traces(fill='toself', line_color='#4C7F3A', fillcolor='#4C7F3A', hoverinfo='all')
    figure.update_layout(
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)  
    )
    
    graph_html_string = pio.to_html(figure, full_html=False)
    return graph_html_string, round(songEnergyAvg, 2), round(songDancibilityAvg, 2), round(songInstrumentalnessAvg, 2), round(songValenceAvg, 2)

def plotTempoData(df): # Return html for tempo bar chart, lowest tempos table, highest tempos table
    tempos = df.loc[:,'songTempo']

    map = {}

    for tempo in tempos:
        if math.isnan(tempo):
            continue
        
        binnedTempo = int(tempo / 10) * 10
        if map.get(binnedTempo):
            map[binnedTempo] += 1
        else:
            map[binnedTempo] = 1

    chartData = pd.DataFrame(map.items(), columns=['Tempo', 'Frequency'])
    chartData = chartData.sort_values(by='Tempo')

    tempoChart = px.bar(chartData, x="Tempo", y="Frequency", title="Track Tempos")
    tempoChart.update_layout(
        xaxis={'tickmode': 'array', 'title': 'Tempo (BPM)', 'tickvals': chartData['Tempo'], 'ticktext': chartData['Tempo']},
        yaxis={'title': 'Frequency'},
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)
    )
    tempoChart.update_traces(marker_color='#4C7F3A')
    tempoChart.update_layout(plot_bgcolor='ghostwhite')
    tempoChartHtml = pio.to_html(tempoChart, full_html=False)

    sortedByMin = df.sort_values(by='songTempo')
    sortedByMax = df.sort_values(by='songTempo', ascending=False)

    tenLowestTempos = sortedByMin[['songName', 'songTempo']].head(10)
    tenHighestTempos = sortedByMax[['songName', 'songTempo']].head(10)

    tenLowestTempos['Rank'] = tenLowestTempos['songTempo'].rank(method='first')
    tenLowestTempos['Rank'] = tenLowestTempos['Rank'].astype(int)
    tenLowestTempos.insert(0, 'Rank', tenLowestTempos.pop('Rank'))
    
    tenHighestTempos['Rank'] = tenHighestTempos['songTempo'].rank(method='first', ascending=False)
    tenHighestTempos['Rank'] = tenHighestTempos['Rank'].astype(int)
    tenHighestTempos.insert(0, 'Rank', tenHighestTempos.pop('Rank'))

    tenLowestTempos.columns = ['Rank', 'Track Name', 'Tempo']
    tenHighestTempos.columns = ['Rank', 'Track Name', 'Tempo']

    lowestTempoTable = tenLowestTempos.to_html(index=False, classes='tempo-chart table table-hover')
    highestTempoTable = tenHighestTempos.to_html(index=False, classes='tempo-chart table table-hover')

    return tempoChartHtml, lowestTempoTable, highestTempoTable

def plotModeGraph(df):
    modes = df.loc[:, 'songKey']

    modeDict = {'Major': 0, 'Minor': 0}

    for mode in modes:
        if mode == 0:
            modeDict['Minor'] += 1
        else:
            modeDict['Major'] += 1

    chartData = pd.DataFrame(modeDict.items(), columns=['Mode', 'Frequency'])

    figure = px.pie(chartData, values='Frequency', names='Mode', title='Track Keys', color_discrete_sequence=['#4C7F3A', 'rgb(55,126,184)'])
    figure.update_layout(
        legend=dict(font=dict(size=20)), 
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23))
    figure.update_traces(textinfo='value+label', insidetextfont=dict(size=20))

    graph_html_string = pio.to_html(figure, full_html=False)
    return graph_html_string

def plotExplicitChart(df):
    chartData = df['isExplicit'].value_counts().reset_index()
    chartData.columns = ['Contains Explicit Lyrics', 'Frequency']

    figure = px.pie(chartData, values='Frequency', names='Contains Explicit Lyrics', title='Track Contains Explicit Lyrics', color_discrete_sequence=['#4C7F3A', 'rgb(55,126,184)'])
    figure.update_layout(
        legend=dict(font=dict(size=20)), 
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)
    )
    figure.update_traces(textinfo='label+value', insidetextfont=dict(size=16), labels=['No', 'Yes'])

    graph_html_string = pio.to_html(figure, full_html=False)
    return graph_html_string

def plotSongBoxPlots(df):
    popularityPlot = px.box(df, y='songPopularity', title='Track Popularity')
    popularityPlot.update_layout(
        yaxis= {'title' : 'Track Popularity'},
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)
    )
    popularityPlot.update_traces(line_color='#4C7F3A', marker=dict(color='#4C7F3A'))

    lengthPlot = px.box(df, y='songLength', title='Track Length')
    lengthPlot.update_layout(
        yaxis= {'title' : 'Track Length (Seconds)'},
        font=dict(family="Roboto", color="black"),
        title_x=0.5,
        title_y=0.95,
        title_font=dict(size=23)
    )
    lengthPlot.update_traces(line_color='#4C7F3A', marker=dict(color='#4C7F3A'))

    popularityPlotHtml = pio.to_html(popularityPlot, full_html=False)
    lengthPlotHtml = pio.to_html(lengthPlot, full_html=False)
    return popularityPlotHtml, lengthPlotHtml