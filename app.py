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
              Output("followers-artist", "children"),
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
    albums = [album_title for album_title in artist_albums.name]
    genres = f"Genres: {' '.join(artist_info['genres'])}"
    followers = f"Followers: {artist_info['followers']}"
    return albums, artist_info['name'], genres, followers, artist_info['image']


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
    table_columns = ['name', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'tempo']
    table_songs = songs[table_columns].copy()
    minutes = (songs['duration_s'] // 60).astype(str).apply(lambda x: x[:-2])
    seconds = (songs['duration_s'] % 60).astype(str).apply(lambda x: x[:-2]).apply(
        lambda x: x if len(x) != 1 else "0" + x)
    table_songs['duration'] = minutes + ":" + seconds
    table_songs.insert(1, 'duration', table_songs.pop('duration'))
    return dash_table.DataTable(id='datatable',
                                data=table_songs.to_dict('records'),
                                columns=[{'name': i, 'id': i} for i in table_songs.columns],
                                page_size=10,
                                fixed_columns={'headers': True, 'data': 1},
                                sort_action='native',
                                tooltip_data=[
                                    {
                                        column: {'value': str(value), 'type': 'markdown'}
                                        for column, value in row.items()
                                    } for row in table_songs.to_dict('records')
                                ],
                                tooltip_duration=None,
                                style_table={'minWidth': '100%'},
                                style_cell={'overflow': 'hidden',
                                            'minWidth': '9.25rem', 'width': '9.25rem', 'maxWidth': '9.25rem',
                                            'textOverflow': 'ellipsis',
                                            'textAlign': 'right',
                                            },
                                style_cell_conditional=[{'if': {'column_id': 'name'},
                                                         'textAlign': 'left',
                                                         'minWidth': '11.25rem',
                                                         'width': '11.25rem',
                                                         'maxWidth': '11.25rem'}]
                                )


app.layout = html.Div([

    navbar,
    main_layout,

])

if __name__ == '__main__':
    app.run_server(debug=True)
