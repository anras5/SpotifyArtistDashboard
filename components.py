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

dropdown_albums = dcc.Dropdown(id="dropdown-albums")

table_songs = dbc.Container(
    id='table-songs',
    children=[]
)
