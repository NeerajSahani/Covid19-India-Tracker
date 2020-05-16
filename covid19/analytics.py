import pandas as pd
from numpy import where
from numpy.distutils.system_info import dfftw_info
from pandas._libs import json
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import requests


def get_data():
    data = pd.read_json('https://api.covid19india.org/state_district_wise.json')
    df = pd.DataFrame()
    for state in data.columns:
        d = pd.DataFrame(data[state].districtData).T
        d['State'] = state
        df = df.append(d, sort=False)
    df['active'] = df['active'].astype(int)
    df['confirmed'] = df['confirmed'].astype(int)
    df['deceased'] = df['deceased'].astype(int)
    df['recovered'] = df['recovered'].astype(int)
    df['District'] = df.index
    return data, df


def get_pie(df, key='State', upto=5):
    df = pd.pivot_table(df, values=['active', 'confirmed', 'recovered', 'deceased'], index=[key], aggfunc=sum)
    df = df.sort_values(by='confirmed', ascending=False)
    pie = go.Figure(
        data=[go.Pie(
            # labels=list(map(statecodes.__getitem__, df.index)),
            labels=df.index[:upto],
            values=df.confirmed[:upto], textinfo='label+value',
            insidetextorientation='radial')]
    )
    config = {
        'displaylogo': False,
        'scrollZoom': True,
        'displayModeBar': False,
    }
    pie.update_layout(
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        showlegend=False,
    )
    return plot(pie, output_type='div', include_plotlyjs=False, config=config)


def get_chart(df, key='District', upto=10):
    df = pd.pivot_table(df, values=['active', 'confirmed', 'recovered', 'deceased'], index=[key], aggfunc=sum)
    df = df.sort_values(by='active', ascending=False)
    df[key] = df.index

    fig = px.bar(df[:upto], x=key, y='active',
                 hover_data=['confirmed', 'recovered', 'active', 'deceased'], color='active',
                 labels={'active': 'Active Cases', key: key}, height=400)

    fig.update_layout(
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=350,
    )
    return plot(fig, output_type='div', include_plotlyjs=False, config={'displaylogo': False})


def get_line_plot():
    data = pd.read_json('https://api.covid19api.com/dayone/country/india')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.Date,
        y=data.Confirmed,
        name='Confirmed',
        mode='lines',
    ))
    fig.add_trace(go.Scatter(
        x=data.Date,
        y=data.Active,
        name='Active',
        mode='lines',
    ))

    fig.add_trace(go.Scatter(
        x=data.Date,
        y=data.Recovered,
        name='Recovered',
        mode='lines',
    ))

    fig.add_trace(go.Scatter(
        x=data.Date,
        y=data.Deaths,
        name='Deaths',
        mode='lines',
    ))

    fig.update_layout(
        template='plotly_white',
        autosize=True,
        height=330,
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            x=0.009,
            y=0.981,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bordercolor="grey",
            bgcolor="white",
            borderwidth=1
        )
    )
    config = {
        'displaylogo': False,
        'scrollZoom': True,
        'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape']
    }
    return plot(fig, output_type='div', include_plotlyjs=False, config=config)


def world_map():
    d = requests.get('https://api.covid19api.com/summary')
    d2 = px.data.gapminder().query("year==2007")
    js = json.loads(d.text)
    df = pd.DataFrame(js['Countries'])
    d2.columns = ['Country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num']
    df = df.merge(d2, on='Country')
    df = df.dropna()
    fig = px.choropleth(df, locations="iso_alpha",
                        color="TotalConfirmed",
                        hover_name="Country",
                        hover_data=['NewConfirmed', 'TotalConfirmed',
                                    'NewDeaths', 'TotalDeaths', 'NewRecovered', 'TotalRecovered'],
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(
        template='plotly_white',
        autosize=True,
        height=360,
        margin=dict(t=0, b=0, l=0, r=0),
        coloraxis_showscale=False,
    )

    config = {
        'displayModeBar': False,
        'displaylogo': False,
        'scrollZoom': True,
    }
    return plot(fig, output_type='div', include_plotlyjs=False, config=config)
