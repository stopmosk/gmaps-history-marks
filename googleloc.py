import pandas as pd

import folium
from folium.plugins import MarkerCluster

import json
from pandas.io.json import json_normalize

#import ijson
#import bigjson


def analyse_map(file):
    # print(json.load(file.stream)['locations'])
    # data = json_normalize(json.load(file.stream)['locations'])

    df = pd.read_json(file)
    # f = open(file)
    # f.readline()
    # df = json.load(file)

    first_dt = pd.to_datetime(int(json_normalize(df[:1]['locations'])['timestampMs']) * 1000000)
    cursor = first_dt.date().day

    # delta = pd.to_datetime('2000-01-02') - pd.to_datetime('2000-01-01')  # 1 day
    # delta3 = pd.to_datetime('2000-01-01 04:00:00') - pd.to_datetime('2000-01-01 00:00:00')  # 4 hours

    data = pd.DataFrame()

    for raw_row in df['locations'][:100]:
        row = json_normalize(raw_row)
        cur_dt = pd.to_datetime(int(row['timestampMs']) * 1000000)

        if cur_dt.date().day != cursor:
            data = pd.concat([data, row], axis=0, join='outer', sort=False)
            print(cursor, cur_dt)
            cursor = cur_dt.date().day

    data['longitude'] = data.longitudeE7 / 10000000
    data['latitude'] = data.latitudeE7 / 10000000
    data.drop(['longitudeE7', 'latitudeE7'], axis=1, inplace=True)

    #if 'altitude' in data.columns:
    #    data.drop(['altitude'], axis=1, inplace=True)
    #if 'verticalAccuracy' in data.columns:
    #    data.drop(['verticalAccuracy'], axis=1, inplace=True)

    data.fillna(0, inplace=True)

    if 'velocity' in data.columns:
        data = data[data['velocity'] == 0]
    if 'accuracy' in data.columns:
        data = data[data['accuracy'] < 1000]

    data = data.set_index(pd.to_datetime(data.timestampMs.map(int) * 1000000)).drop('timestampMs', axis=1)
    data.index.name = 'time'

    # dmt = data.resample('10T').last().dropna(how='all')
    # dhr = data.resample('H').last().dropna(how='all')
    # dh12 = data.resample('12H').last().dropna(how='all')
    # ddy = data.resample('D').last().dropna(how='all')

    ddy = data

    def getmap(data, radius=5, color='red', opacity=0.9, zoom=12, cluster=False):

        map = folium.Map(location=[data.latitude.median(), data.longitude.median(), ], zoom_start=zoom)
        lat, lon = data.latitude, data.longitude
        date = data.index

        if cluster:
            final_map = MarkerCluster().add_to(map)
        else:
            final_map = map

        for lat, lon in zip(lat, lon):
            folium.CircleMarker(location=(lat, lon),
                                radius=radius,
                                stroke=False,
                                fill_color=color,
                                fill_opacity=opacity).add_to(final_map)

        return map

    # Вариант с кластерами
    #getmap(ddy, radius=5, color='red', opacity=0.05, zoom=10, cluster=True)

    return getmap(ddy)
