"""
Main display script of the movie recommender web interface
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import grab_list
from simple_recommender import SimpleRecommendation
from content_based import ContentRecommendation
from app import APP
from grab_list import object_save
from userbased_filtering import Collaborative
import display_popularity
import display_content_base
import display_recomm
#import display_final_movie


# we use the Row and Col components to construct the SIDEBAR header
# it consists of a title, and a toggle, the latter is hidden on large screens
SIDEBARHEADER = dbc.Row(
    [
        dbc.Col(html.H2("Movie Recommender", className="display-5")),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

SIDEBAR = html.Div(
    [
        SIDEBARHEADER,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr()
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Simple Filtering",
                                href="/page-simple-filtering",
                                id="page-simple-filtering-link",
                                style={'font-size': '13px'}),
                    dbc.NavLink("Content-based Filtering",
                                href="/page-content-based-filtering",
                                id="page-content-based-filtering-link",
                                style={'font-size': '13px'}),
                    dbc.NavLink("User-based Filtering",
                                href="/page-user-based-filtering",
                                id="page-user-based-filtering-link",
                                style={'font-size': '13px'})
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)


CONTENT = dcc.Loading(id="loading-page-main",
                      children=[
                          html.Div(id="page-content")],
                      # type='dot',
                      fullscreen=True,
                      color='#2B60DE')

APP.layout = html.Div([dcc.Location(id="url"), SIDEBAR, CONTENT])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
PAGENAMES = ['simple-filtering', 'content-based-filtering', 'user-based-filtering']
@APP.callback(
    [Output(f"page-{page_name}-link", "active") for page_name in PAGENAMES],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    """
    call back to display multiple pages with the first page being default
    :param pathname: url of the pages
    :return: a list of pathname of the pages
    """
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{page_name}" for page_name in PAGENAMES]


@APP.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    """
    render each page
    :param pathname: path of the page to be rendered
    :return: the corresponding html div of the page to be displayed
    """
    if pathname in ["/", "/page-simple-filtering"]:
        # return
        app_popularity_tab = display_popularity.main()
        return app_popularity_tab
    elif pathname == "/page-content-based-filtering":
        # return
        app_filter_tab = display_content_base.main()
        return app_filter_tab
    elif pathname == "/page-user-based-filtering":
        # return
        app_recommender_tab = display_recomm.main()
        return app_recommender_tab
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ]
    )


display_popularity.call_back_popularity_filter()
display_content_base.call_back_filter()
display_recomm.call_back_recom()


@APP.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    """
    collapse the side bar
    """
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    APP.run_server(debug=False)
