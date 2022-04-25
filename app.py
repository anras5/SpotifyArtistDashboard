from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import search_spotipy

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.H1("Spotify Artist Dashboard", style={'text-align': 'center'}),

    dcc.Input(id="input_artist", placeholder="Search for your artist"),

    html.Div(id='output_container', children=[]),
    html.Br(),

])


@app.callback(Output("output_container", "children"),
              Input("input_artist", "value"))
def get_artist_info(name):
    if name:
        artist_info = search_spotipy.get_artist_info(name)
        return f"{artist_info['name']} has {artist_info['followers']} followers"
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
