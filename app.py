from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import search_spotipy
from components import navbar, main_layout
from dash.exceptions import PreventUpdate

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])


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
              Output("chosen-artist", "children"),
              Output("genres-artist", "children"),
              Output("photo-artist", "src"),
              Input("button-artist", "n_clicks"),
              State("input-artist", "value"))
def show_albums(n_clicks, artist_name):
    if not artist_name:
        raise PreventUpdate
    artist_info = search_spotipy.get_artist_info(artist_name)
    # print(artist_info)
    artist_albums = search_spotipy.get_artist_albums(artist_info['id'])
    # print([album_title for album_title in artist_albums.name])
    return [album_title for album_title in artist_albums.name], artist_info['name'], ' '.join(artist_info['genres']), \
           artist_info['image']


@app.callback(Output("table-songs", "children"),
              Input("dropdown-albums", 'value'),
              State("chosen-artist", "children"))
def show_songs(album_name, artist_name):
    if not album_name or not artist_name:
        raise PreventUpdate
    artist_info = search_spotipy.get_artist_info(artist_name)
    artist_albums = search_spotipy.get_artist_albums(artist_info['id'])
    chosen_album = artist_albums[artist_albums.name == album_name]
    # print(chosen_album['id'][0])
    songs = search_spotipy.get_album_tracks(chosen_album['id'][0])
    table_columns = ['name', 'duration_ms']
    table_songs = songs[table_columns]
    return dash_table.DataTable(data=table_songs.to_dict('records'),
                                columns=[{'name': i, 'id': i} for i in table_columns],
                                page_action='none',
                                style_table={'height': '300px', 'overflowY': 'auto'})


app.layout = html.Div([

    navbar,
    main_layout,

])

if __name__ == '__main__':
    app.run_server(debug=True)
