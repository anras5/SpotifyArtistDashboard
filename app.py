from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import search_spotipy
from components import navbar, table_songs, dropdown_albums
from dash.exceptions import PreventUpdate

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("dropdown-albums", "options"),
              Input("button-artist", "n_clicks"),
              State("input-artist", "value"))
def show_albums(n_clicks, artist_name):
    if not artist_name:
        raise PreventUpdate
    artist_info = search_spotipy.get_artist_info(artist_name)
    artist_albums = search_spotipy.get_artist_albums(artist_info['id'])
    print([album_title for album_title in artist_albums.name])
    return [album_title for album_title in artist_albums.name]


@app.callback(Output("table-songs", "children"),
              Input("dropdown-albums", 'value'),
              State("input-artist", "value"))
def show_songs(album_name, artist_name):
    if not album_name or not artist_name:
        raise PreventUpdate
    artist_info = search_spotipy.get_artist_info(artist_name)
    artist_albums = search_spotipy.get_artist_albums(artist_info['id'])
    chosen_album = artist_albums[artist_albums.name == album_name]
    print(chosen_album['id'][0])
    return dash_table.DataTable(search_spotipy.get_album_tracks(chosen_album['id'][0]))


app.layout = html.Div([

    navbar,
    dropdown_albums,
    html.Br(),
    table_songs

])

if __name__ == '__main__':
    app.run_server(debug=True)
