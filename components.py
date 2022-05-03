import dash_bootstrap_components as dbc
from dash import dcc, html

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id="input-artist", type="search", placeholder="Search")),
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

main_layout = dbc.Container([

    dbc.Row([

        # artist panel
        dbc.Col([

            dbc.Row(html.H3("Choose your favorite artist",
                            id='chosen-artist',
                            className='text-center')),

            dbc.Row(html.Div("Genres",
                             id='genres-artist',
                             className='text-center')),

            dbc.Row(html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/2048px"
                    "-Spotify_logo_without_text.svg.png",
                id='photo-artist',
                className='img-fluid')),

        ],
            lg=4, md=12, sm=12),

        # Album choosing panel + datatable
        dbc.Col([

            dbc.Row(dcc.Dropdown(id="dropdown-albums",
                                 className="my-4")),

            dbc.Row(dbc.Container(id='table-songs',
                                  children=[],
                                  className="mx-4 my-1 justify-content-center"))

        ],
            lg=8, md=12, sm=12,
            class_name='my-2')

    ],
        class_name='mx-4 my-4')
])
