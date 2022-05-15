import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import search_spotipy
import plots
from components import main_layout
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


@app.callback(
    Output("dropdown-albums", "options"),
    Output("chosen-artist", "children"),
    Output("genres-artist", "children"),
    Output("followers-artist", "children"),
    Output("id-artist", "children"),
    Output("photo-artist", "src"),
    Input("button-artist", "n_clicks"),
    State("input-artist", "value"))
def show_albums(n_clicks, artist_name):
    if not artist_name:
        raise PreventUpdate
    artist_info = search_spotipy.get_artist_info(artist_name)
    artist_albums = search_spotipy.get_artist_albums(artist_info['id'])
    albums = [{'label': album.name, 'value': album.id} for album in artist_albums.itertuples()]
    genres = f"Genres: {' '.join(artist_info['genres'])}"
    followers = f"Followers: {artist_info['followers']}"
    artist_id = f"ID: {artist_info['id']}"
    return albums, artist_info['name'], genres, followers, artist_id, artist_info['image']


@app.callback(Output("table-songs", "children"),
              Input("dropdown-albums", "value"),
              Input("button-artist", "n_clicks"),
              State("chosen-artist", "children"))
def update_datatable(chosen_album_id, artist_name, n_clicks):
    if not chosen_album_id or not artist_name:
        raise PreventUpdate
    triggered_id = callback_context.triggered[0]['prop_id']
    if triggered_id == 'button-artist.n_clicks':
        return clear_datatable()
    else:
        return show_datatable(chosen_album_id, artist_name)


def clear_datatable():
    print('clear')
    return dash_table.DataTable(id='datatable', data=[])


def show_datatable(chosen_album_id, artist_name):
    if not chosen_album_id or not artist_name:
        raise PreventUpdate
    songs = search_spotipy.get_album_tracks(chosen_album_id)
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
                                page_size=9,
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


@app.callback(
    Output('bar-plot', 'figure'),
    Input('dropdown-bar-plot', 'value'),
    Input('datatable', 'derived_virtual_data'),
    Input('button-artist', 'n_clicks'),
    prevent_initial_call=True
)
def update_bar_plot(chosen_type, data, n_clicks):
    if not chosen_type or not data:
        raise PreventUpdate
    triggered_id = callback_context.triggered[0]['prop_id']
    if triggered_id == 'button-artist.n_clicks':
        return plots.reset_bar_plot()
    else:
        return plots.create_bar_plot(chosen_type, data)


@app.callback(
    Output('scatter-plot', 'figure'),
    Input('dropdown-scatter-first', 'value'),
    Input('dropdown-scatter-second', 'value'),
    Input('datatable', 'derived_virtual_data'),
    Input('button-artist', 'n_clicks')
)
def update_scatter_plot(x_axis, y_axis, data, n_clicks):
    if not x_axis or not y_axis or not data:
        raise PreventUpdate
    triggered_id = callback_context.triggered[0]['prop_id']
    if triggered_id == 'button-artist.n_clicks':
        return plots.reset_scatter_plot()
    else:
        return plots.create_scatter_plot(x_axis, y_axis, data)


@app.callback(Output("dropdown-box", "options"),
              Input("dropdown-albums", "value"),
              State("id-artist", "children"))
def display_not_chosen_albums(chosen_album, artist_id):
    if not chosen_album or not artist_id:
        raise PreventUpdate
    artist_id = artist_id.split()[1]
    artist_albums = search_spotipy.get_artist_albums(artist_id)
    not_chosen_albums = [{'label': album.name, 'value': album.id} for album in artist_albums.itertuples()
                         if album.id != chosen_album]
    return not_chosen_albums


@app.callback(
    Output('box-plot', 'figure'),
    Input('dropdown-box', 'value'),
    Input('datatable', 'derived_virtual_data'),
    Input('button-artist', 'n_clicks')
)
def update_box_plot(compare_album_id, album_1_data, n_clicks):
    if not compare_album_id or not album_1_data:
        raise PreventUpdate
    triggered_id = callback_context.triggered[0]['prop_id']
    if triggered_id == 'button-artist.n_clicks':
        return plots.reset_box_plot()
    else:
        return plots.create_box_plot(compare_album_id, album_1_data)


app.layout = main_layout

if __name__ == '__main__':
    app.run_server(debug=True)
