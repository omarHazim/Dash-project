# Import supporting lib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly.graph_objs as go
import pandas as pd
import flask
from geopy.geocoders import Nominatim
import itertools
from itertools import *
import os
import numpy as np
from dash.dependencies import Input, Output, State, Event
#import json

# Creating the Dash App

## Reading the dataset in '.xlsx' file
def import_excel(
    xlxs_file_nme, sheet_num ,col_nme = '' , sheet_idx=False, file_loc=True):
    """
    Import and convert .xlxs file to a dataframe
    Inputs:
    ________________
     - xlxs_file_nme: str
         .xlxs file name
     - sheet_num: int / str
         name (or number) of the sheet inside .xlxs
     - col_nme: str
         when sheet_idx is "True", add column name to set dataframe index
     - sheet_idx: bol
         set dataframe index according to any specified column within the datframe , default "False"
     - file_loc:
    Outputs:
    ________________
     - dataframe of dataset
    """
    if file_loc:
        file_path = os.path.abspath(xlxs_file_nme)
        xlsx = pd.ExcelFile(file_path)
        sheet1 = xlsx.parse(sheet_num)
        if sheet_idx:
            sheet1.index = sheet1[col_nme]
            new_df_beach_0 = sheet1.iloc[:]
            new_df_beach_0.fillna(value= 'NaN', inplace=True)
            return new_df_beach_0
        else:
            new_df_beach_0 = sheet1.iloc[:]
            new_df_beach_0.reset_index(inplace= True)
            new_df_beach_0.drop(['index'], axis=1, inplace = True)
            new_df_beach_0.fillna(value= 'NaN', inplace=True)
            return new_df_beach_0
    else:
        xlsx = pd.ExcelFile(xlxs_file_nme)
        sheet1 = xlsx.parse(sheet_num)
        if sheet_idx:
            sheet1.index =  sheet1[col_nme]
            new_df_beach_0 = sheet1.iloc[:]
            new_df_beach_0.fillna(value= 'NaN', inplace=True)
            return new_df_beach_0
        else:
            new_df_beach_0 = sheet1.iloc[:]
            new_df_beach_0.reset_index(inplace= True)
            new_df_beach_0.drop(['index'], axis=1, inplace = True)
            new_df_beach_0.fillna(value= 'NaN', inplace=True)
            return new_df_beach_0

## Add different info to the map marker
def df_map(
    df, location_col, name_col, beach, proj, client, status,
    deadline, code):
    def poptext_3(
        df, location_col, name_col, beach, proj, client, status,
        deadline, code, x):

        new_df = df[
            [location_col, name_col, beach, proj, client, status,
             deadline, code]
        ].groupby([location_col, name_col, beach, proj, client, status,
                   deadline, code]).count()
        info_lst = []
        for info in new_df.index:
            if info[0] == x:
                yield 'Name: {0} , Beach: {1} , Project: {2}, Client: {3},\
                Status: {4}, Deadline: {5} , Case code: {6}'.format(
                    info[1], info[2], info[3], info[4], info[5],
                    info[6].date(), info[7])

    geolocator = Nominatim()
    countries = pd.DataFrame({'country': list(set(df[location_col]))})
    countries['lat'] = countries['country'].apply(
    lambda x: geolocator.geocode(x, timeout=15).latitude)
    countries['lon'] = countries['country'].apply(
    lambda x: geolocator.geocode(x, timeout=15).longitude)
    countries['Avrg_Days_till_Deadline'] = df.groupby(['Location'])[
        'Days until DL'].mean().round(decimals=0).values
    countries['info'] = countries['country'].apply(lambda i: list(poptext_3(
    df,location_col, name_col, beach, proj, client, status,
        deadline, code, i)))
    return countries
app = dash.Dash()

mapbox_access_token = 'pk.eyJ1Ijoib21hcmhhemltIiwiYSI6ImNqY2s5cHk3MzNyZDEycm1tanV6c3pzdGUifQ.hLOK6z98WohsI19MmNBiHw'


# Boostrap CSS.
#app.config['suppress_callback_exceptions']=True
app.css.append_css(
    {'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Team activity / OW-STHLM office',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)
app.layout = html.Div([
    html.Div(
        [dcc.Graph(id='map-graph',style={'margin-top': '20'})
        ], className = "six columns"
    ),
    html.Div([dt.DataTable(
        rows=map_data.to_dict('records'),
        columns=map_data.columns,
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable'),]
             , style="light",
             className="six columns")]
)


@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])

def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.loc[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)
def gen_map(map_data):
    return {
        "data": [{
            "type": "scattermapbox",
            "lat": list(map_data['lat']),
            "lon": list(map_data['lon']),
            #"text": list(onverted_df['Need Score']),
            "mode": "markers",
            "name": list(map_data['country']),
            "marker": {
                "size": 6,
                "opacity": 1.0,
                "color": color_scale(map_data)
            }
        }
        ],
        "layout": layout
    }

if __name__ == '__main__':
    # Builidng Dash/plotly app
    new_df_beach = import_excel(
        'https://github.com/omarHazim/OmarHazim/blob/master/ow_dash_project/Copy%20of%20Beach%20Work%20HTMLversion.xlsx', sheet_num=0, sheet_idx = False
    ) #, sheet_idx='Name'
    converted_df = df_map(new_df_beach,'Location', 'Name','Beach','Project' ,
                          'Client', 'Status' , 'Deadline', 'Case code')
    app.run_server(debug=True)
