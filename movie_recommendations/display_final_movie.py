"""
This file is a helper function to add movie html div to front end display
"""
import dash_html_components as html
import get_movie_info

COLORS = {
    'background': '#111111',
    'text': '#000000'
}


def get_info(item_json):
    """
    get movie information from the json return from the API
    :param item_json: a movie information json from the TMDB API
    :return: name, poster, overview, vote_average,
             release_date, runtime, popularity, genres_div of the movie
    """
    name = item_json[get_movie_info.MovieJsonKeys.name]
    poster = get_movie_info.POSTER_URL_CONSTANT + item_json[get_movie_info.MovieJsonKeys.poster_url]
    overview = item_json[get_movie_info.MovieJsonKeys.overview]
    vote_average = item_json[get_movie_info.MovieJsonKeys.vote_average]
    list_genres = item_json[get_movie_info.MovieJsonKeys.genres]
    if len(list_genres) > 5:
        genres1 = ', '.join([elem['name'] for elem in list_genres[:4]]) + ','
        genres2 = ', '.join([elem['name'] for elem in list_genres[4:]])
        genres_div = html.Div(children=[
            html.Div(children='Genres:', className='alignleft'),
            html.Div(children=f'{genres1}', className='alignright'),
            html.Div(children=f'{genres2}', className='alignright')],
                              style={'clear': 'both'})
    else:
        genres = ', '.join([elem['name'] for elem in list_genres])
        genres_div = html.Div(children=[
            html.Div(children='Genres:', className='alignleft'),
            html.Div(children=f'{genres}', className='alignright')],
                              style={'clear': 'both'})
    release_date = item_json[get_movie_info.MovieJsonKeys.release_date]
    popularity = item_json[get_movie_info.MovieJsonKeys.popularity]
    runtime = item_json[get_movie_info.MovieJsonKeys.runtime]
    return name, poster, overview, vote_average, release_date, runtime, popularity, genres_div


def add_final_movies(zipped_list):
    """
    integrate the name, poster, overview, vote_average,
    release_date, runtime, popularity, genres_div of a movie into
    a html div, which can be display in the front end
    :param zipped_list: a list of movie ids with their corresponding
           indices being 1, 2, ..., # of movie ids in the list
    :return: a html div to be displayed
    """
    result = []
    for item in zipped_list:
        item_index = item[0]
        item_movie_id = item[1]
        item_json = get_movie_info.get_movie_json(item_movie_id)
        try:
            name, poster, overview, vote_average, release_date, \
            runtime, popularity, genres_div = get_info(item_json)
        except (TypeError, KeyError):
            continue
        result.append(
            html.Div([
                html.Div(
                    id='movie_title_{}'.format(item_index),
                    children=name,
                    style={
                        'font-size': '15px',
                        'margin': '5px',
                        'textAlign': 'center',
                        'color': COLORS['text']}),
                html.Div(
                    className='container',
                    children=[html.Img(className='image',
                                       id='image_{}'.format(item_index),
                                       src=poster,
                                       style={'height': '410px'}),
                              html.Div(className='middle',
                                       children=html.Div(
                                           className='text',
                                           children=f'Movie overview: {overview}',
                                           style={'font-size': '13px'}),
                                       style={'transform': 'translate(-2.5%, -100%)'})]),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children='Average vote:', className='alignleft'),
                        html.Div(f'{vote_average}', className='alignright')],
                             style={'clear': 'both'}),
                    genres_div,
                    html.Div(children=[
                        html.Div(children='Release Date: ', className='alignleft'),
                        html.Div(children=f'{release_date}', className='alignright')],
                             style={'clear': 'both'}),
                    html.Div(children=[
                        html.Div(children='Popularity: ', className='alignleft'),
                        html.Div(children=f'{popularity}', className='alignright')],
                             style={'clear': 'both'}),
                    html.Div(children=[
                        html.Div(children='Runtime: ', className='alignleft'),
                        html.Div(children=f'{runtime}', className='alignright')],
                             style={'clear': 'both'})],
                         style={'width': '90%',
                                'margin-left': '5%',
                                'margin-right': '5%'})],
                     style={'margin': '15px',
                            'margin-top': '80px',
                            'width': '30%',
                            'display': 'inline-block'}))
    return result
