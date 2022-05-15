import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

SCATTER_OPTIONS = ['danceability', 'energy', 'loudness',
                   'speechiness', 'acousticness', 'instrumentalness',
                   'liveness', 'tempo']
BAR_OPTIONS = ['duration', 'danceability', 'energy']

BACKGROUND_COLOR = "#125B50"
DROPDOWN_COLOR = "#FAF5E4"


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id="input-artist", type="search", placeholder="Search for artist")),
        dbc.Col(
            dbc.Button(
                "Search", id="button-artist", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Spotify Artists Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

artist_info_and_table = dbc.Container([

    dbc.Row([

        # artist panel
        dbc.Col([

            dbc.Row(html.H3("Use search bar to choose your favorite artist",
                            id='chosen-artist',
                            className='text-center')),

            dbc.Row(html.Div("Genres",
                             id='genres-artist',
                             className='text-center')),

            dbc.Row(html.Div("Followers",
                             id='followers-artist',
                             className='text-center')),

            dbc.Row(html.Div("ID",
                             id='id-artist',
                             className='text-center')),

            dbc.Row(html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/2048px"
                    "-Spotify_logo_without_text.svg.png",
                id='photo-artist',
                className='img-fluid'),
                class_name='mx-5 my-5'),

        ],
            lg=4, md=12, sm=12),

        # Album choosing panel + datatable
        dbc.Col([

            dbc.Row(dcc.Dropdown(id="dropdown-albums", placeholder="Choose album"),
                    class_name='px-1 my-3'),

            dbc.Row(dbc.Container(id='table-songs',
                                  children=[dash_table.DataTable(id='datatable')],
                                  className="my-1 justify-content-center"),
                    class_name='px-1 my-3')

        ],
            lg=8, md=12, sm=12,
            class_name='my-2')

    ],
        class_name='mx-4 my-4')
])

graph_layout = dbc.Container([

    # First row
    dbc.Row([

        # BAR-PLOT
        dbc.Col([
            html.Div("Choose feature for the bar chart",
                     id='bar-plot-description',
                     className='text-center'),
            dcc.Dropdown(id='dropdown-bar-plot', options=BAR_OPTIONS),
            dcc.Graph(id='bar-plot', figure={})
        ],
            lg=6, md=12, sm=12
        ),

        # SCATTER-PLOT
        dbc.Col([
            html.Div("Choose features for the scatter plot",
                     id='scatter-plot-description',
                     className='text-center'),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='dropdown-scatter-first', options=SCATTER_OPTIONS)),
                dbc.Col(dcc.Dropdown(id='dropdown-scatter-second', options=SCATTER_OPTIONS))
            ]),
            dcc.Graph(id='scatter-plot', figure={})],
            lg=6, md=12, sm=12
        )

    ]),

    # Second row
    dbc.Row([

        # BOX-PLOT
        dbc.Col([
            html.Div("Choose album and feature to compare on the box plot",
                     id='box-plot-description',
                     className='text-center'),
            dcc.Dropdown(id='dropdown-box', options=[]),
            dcc.Graph(id='box-plot', figure={})
        ],
            lg=12
        )

    ])

])

main_layout = html.Div(
    [
        navbar,
        artist_info_and_table,
        graph_layout
    ],
)

