import pandas as pd
import plotly.express as px
import search_spotipy


def reset_bar_plot():
    return {}


def create_bar_plot(chosen_type, data):
    dff = pd.DataFrame(data)[[chosen_type, 'name']]
    dff.reset_index(inplace=True)
    if chosen_type == 'duration':
        dfff = dff['duration'].str.split(':', expand=True)
        dff['time'] = dfff[0].astype(int) * 60 + dfff[1].astype(int)
        max_time = dff['time'].max()
        ticktexts = []
        for i in range(0, max_time + 30, 30):
            minutes, seconds = tuple(map(str, divmod(i, 60)))
            if len(seconds) == 1:
                seconds = '0' + seconds
            ticktexts.append(f'{minutes}:{seconds}')
        fig_bar = px.bar(dff, x=dff['index'], y=dff['time'],
                         hover_data={'index': False, 'time': False, 'duration': True, 'name': True})
        fig_bar.update_xaxes(title='Number of song on album')
        fig_bar.update_yaxes(title='Duration', tickmode='array', tickvals=list(range(0, max_time + 30, 30)),
                             ticktext=ticktexts, dtick=30)
    else:
        fig_bar = px.bar(dff, x=dff['index'], y=dff[chosen_type],
                         hover_data={'index': False, 'name': True})
        fig_bar.update_xaxes(title='Number of song on album')

    return fig_bar


def reset_scatter_plot():
    return {}


def create_scatter_plot(x_axis, y_axis, data):
    if x_axis == y_axis:
        dff = pd.DataFrame(data)[[x_axis, 'name']]
        fig_scatter = px.scatter(dff, x=dff[x_axis], y=dff[x_axis], hover_data={'name': True})
        return fig_scatter
    else:
        dff = pd.DataFrame(data)[[x_axis, y_axis, 'name']]
        fig_scatter = px.scatter(dff, x=dff[x_axis], y=dff[y_axis], hover_data={'name': True})
        return fig_scatter


def reset_box_plot():
    return {}


def create_box_plot(compare_album_id, album_1_data):
    df_album_1 = pd.DataFrame(album_1_data)
    df_album_2 = search_spotipy.get_album_tracks(compare_album_id)
    df_album_1['choose'] = 0
    df_album_2['choose'] = 1
    dff = pd.concat([df_album_1, df_album_2])
    fig_box = px.box(dff, y='energy', color='choose')
    return fig_box
