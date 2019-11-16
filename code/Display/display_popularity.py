import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np

from app import app
import display_final_movie
import global_record

num_movie_rate = 8
num_final_recommend = 10

colors = {
    'background': '#111111',
    'text': '#000080'
}

filter_options = ['Genre', 'Year', 'Country', 'Director', 'Actors']

year_val = [{'label': 'All', 'value': 'All'}]
year_val.extend([{'label': str(i), 'value': i} for i in np.arange(1970, 2017, 1)])


def add_popularity_filter():
    movie_div = display_final_movie.add_final_movies(zip(range(num_final_recommend),
                                                         global_record.initial_movie_id_list[10:(10+num_final_recommend)]))
    filter_drop_down = []
    for f in filter_options:
        filter_drop_down.append(html.Div(
            children=[
                html.Div("Please Select a {}".format(f),
                         style={'text-align': 'center',
                                'font-size': '12px'}),
                dcc.Dropdown(
                    id=f,
                    options=year_val,
                    value="All",
                    # multi=True,
                    placeholder="Please select a year")],
            style={
                'width': '15%',
                'margin-left': '4%',
                # 'padding-left': '10%',
                # 'padding-right': '10%',
                'display': 'inline-block',
                'color': colors['text']}))

    app_popularity_tab = html.Div(children=[])
    app_popularity_tab.children.append(html.Div(filter_drop_down, style={'margin-top': '50px'}))
    filter_button_div = html.Div(html.Button(id='popularity_filter_button', children='Filter'),
                                 style={'margin-top': '50px',
                                        'margin-bottom': '100px',
                                        'width': '40%',
                                        'padding-left': '45%',
                                        'padding-right': '15%'})
    app_popularity_tab.children.append(filter_button_div)
    app_popularity_tab.children.append(html.Div("List of movies:"))
    app_popularity_tab.children.append(html.Div(id='popularity_main_div', children=movie_div))
    return app_popularity_tab


def call_back_popularity_filter():
    list_state = [State(f'{f}', 'value') for f in filter_options]
    @app.callback(
        Output('popularity_main_div', 'children'),
        [Input('popularity_filter_button', 'n_clicks')],
        list_state)
    def update_multi_output(n_clicks, *input_value):
        ctx = dash.callback_context
        if not ctx.triggered:
            user_click = 'No clicks yet'
        else:
            user_click = ctx.triggered[0]['prop_id'].split('.')[0]
        if n_clicks is not None and n_clicks > 0:
            list_filter = list(input_value)
            # TODO: call backend to filter here (param is a list: 'Genre', 'Year', 'Country', 'Director', 'Actors')
            list_next_movie_id = [862 if r == 2000 else 2 for r in list_filter]
            result = display_final_movie.add_final_movies(zip(range(5), list_next_movie_id))
            return result
        else:
            raise PreventUpdate


def main():
    return add_popularity_filter()


if __name__ == "__main__":
    main()