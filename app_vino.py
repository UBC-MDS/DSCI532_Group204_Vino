import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
# from vega_datasets import data
import states_choropleth
import state_choropleth
from varieties_heatmap import plot_heatmap
from bar_plots import sort_extract_bar_plot
import dash_bootstrap_components as dbc

alt.data_transformers.disable_max_rows()

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.LUX,
                                                                        'jumbotron.css'])

# app = dash.Dash(__name__)
server = app.server

app.title = "V is for Vino"

data = pd.read_csv('data/cleaned_data.csv', index_col=0)

# Get the states dictionary
STATES = data[['state', 'state_id']].drop_duplicates(keep='first')
STATES.rename(columns={"state": "label", "state_id": "value"}, inplace=True)
STATES = STATES.to_dict('records')

def plot_choropleth(_type, state_id=6):
    """
    Helper function to call the correct Choropleth mapping.

    Parameters:
    -----------
    _type -- (str) string of either 'states' or 'state'.
    state_id -- (int) a state_id (ex. 6 for 'California' - default of 6)
    """
    if _type == 'states':
        return states_choropleth.plot_map(data)
    elif _type == 'state':
        return state_choropleth.plot_map(data, state_id)

jumbotron = dbc.Jumbotron(
    [
        dbc.Col(
            [
                # html.Img(src='https://images.pexels.com/photos/391213/pexels-photo-391213.jpeg?cs=srgb&dl=action-alcohol-art-beverage-391213.jpg&fm=jpg', 
                #       width='100px'),
                html.H1("V is for Vino", className="display-3"),
                html.P(
                    "Explore the best wines the United States has to offer using our interactive dashboard",
                    className="lead",
                ),

            ],
            style={"text-align": 'center'})],
    fluid=True,
)

content = dbc.Container([
        html.P(
            "This app allows you visualize details of over 50,000 wine reviews from across \
            the United States, using data scraped from Wine Enthusiast on November 22nd, \
            2017. Given the data source, the wines tend to be of relatively high quality, \
            with each receiving a rating score between 80 and 100. \
            We’ve used these ratings to assign a ‘value’ score to each wine, which \
            is essentially a ratio of its rating to price. Each review also contains details \
            such as grape variety, winery, region, county, and state."
        ),
        html.Br(),
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Geographic Analysis',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                                dbc.Row([
                                    dbc.Col(html.Br())
                                ]),
                                dbc.Row([
                                    dbc.Col(html.Br())
                                ]),
                                dbc.Row([
                                    dbc.Col(html.H1('Wine Reviews by Geographic Location'))
                                ]),
                                dbc.Row([
                                    dbc.Col(html.Br())
                                ]),
                                dbc.Row([
                                    dbc.Col(html.P("See how wine is distributed across the U.S. \
                                          Hover over a particular state or county to see some summary \
                                          information for things like average price, points, or value rating. \
                                          Use the dropdown menu to take a closer look at a particular state, \
                                          where you can see a breakdown by county. Hover over a county to get more \
                                          summary information. In no time at all you'll be an expert on where you can \
                                          find the best wine's at the best prices in America."))
                                ]),
                                dbc.Row([
                                    dbc.Col(html.Br())
                                ]),
                                dbc.Row([
                                    dbc.Col(html.H3('Total Number of Reviews'))
                                ]),
                                dbc.Row(
                                    dbc.Col(html.Hr(hidden=False,
                                                    style={'height':1,
                                                           'background-color': '#50107a',
                                                           'margin-top': 0}))
                                ),
                                dbc.Row([
                                    dbc.Col(html.H5('Choose a State'))
                                ]),
                                dbc.Row([
                                    dcc.Dropdown(
                                        id='state_id',
                                        options=STATES,
                                        value=6, 
                                        style=dict(width='45%',
                                                   verticalAlign='middle',
                                                   left=15)
                                    )
                                ]),
                                dbc.Row([
                                    html.Iframe(
                                        sandbox='allow-scripts',
                                        id='state_choropleth',
                                        height=500,
                                        width=420,
                                        style={'border-width': '0'},
                                        srcDoc=plot_choropleth('state').to_html()),
                                    html.Iframe(
                                        sandbox='allow-scripts',
                                        id='states_choropleth',
                                        height=500,
                                        width=720,
                                        style={'border-width': '0'},
                                        srcDoc=plot_choropleth('states').to_html())
                                ]),
                            ]
                ),
                dcc.Tab(
                    label='Explore Rating, Price & Value of Wines',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children = [
                        dbc.Row([
                                dbc.Col(html.Br())
                            ]),
                         dbc.Row([
                                dbc.Col(html.Br())
                            ]),
                        dbc.Row([
                                dbc.Col(html.H1('Wine Feature Comparisons'))
                            ]),
                        dbc.Row([
                                dbc.Col(html.Br())
                            ]),
                        dbc.Row([
                                dbc.Col(html.P('These interactive graphs allow you to explore the price, rating and value for different \
                                wineries, grape varieties, and regions. The bar chart shows dynamically ranked \
                                results for calculated averages, while the heat map shows the distribution \
                                of value (scaled rating / dollar) for popular grape varieties.'))
                            ]),
                        dbc.Row([
                                dbc.Col(html.Br())
                            ]),
                        dbc.Row([
                                dbc.Col(html.H3('Wine Rankings'))
                            ]),
                        dbc.Row(
                            dbc.Col(html.Hr(hidden=False,
                                            style={'height':1,
                                                   'background-color': '#50107a',
                                                   'margin-top': 0}))
                        ),
                        dbc.Row([
                                dbc.Col(html.H5('Choose X Axis:')),
                                dbc.Col(html.H5('Choose Y Axis:')),
                                dbc.Col(html.H5('Choose Ranking:')),
                            ]),
                        dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='bar-chart-x',
                                        options=[
                                            {'label': 'Region', 'value': 'region_1'},
                                            {'label': 'Winery', 'value': 'winery'},
                                            {'label': 'Grape Variety', 'value': 'variety'},
                                        ],
                                        value='region_1', # setting default when app loads
                                        style=dict(width='80%',
                                                verticalAlign='middle')
                                        )),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='bar-chart-y',
                                        options=[
                                            {'label': 'Rating', 'value': 'points'},
                                            {'label': 'Price', 'value': 'price'},
                                            {'label': 'Value', 'value': 'value_scaled'},
                                        ],
                                        value='points',
                                        style=dict(width='80%',
                                                verticalAlign='middle')
                                        )),
                                dbc.Col(
                                    dcc.RadioItems(
                                        id='bar-chart-sort',
                                        options=[
                                            {'label': ' Lowest to Highest  ', 'value': 'asc'},
                                            {'label': ' Highest to Lowest', 'value': 'desc'}
                                        ],
                                        value='asc',
                                        labelStyle={'display': 'block'}
                                        )),
                            ]),
                        dbc.Row([
                                dbc.Col(html.H5('Number of observations:'))
                            ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Slider(
                                    id='bar-chart-slider',
                                    min=1,
                                    max=50,
                                    step=1,
                                    value=15,
                                    marks={
                                        1: {'label': '1'},
                                        5: {'label': '5'},
                                        10: {'label': '10'},
                                        15: {'label': '15'},
                                        20: {'label': '20'},
                                        25: {'label': '25'},
                                        30: {'label': '30'},
                                        35: {'label': '35'},
                                        40: {'label': '40'},
                                        45: {'label': '45'},
                                        50: {'label': '50'},
                                    }
                                ),
                            ],
                            style={'marginBottom': 50, 'marginTop': 10}),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    sandbox='allow-scripts',
                                    id='plot',
                                    height=600,
                                    width=800,
                                    style={'border-width': '0'},
                                    ### Link this Iframe to the dynamic bar plot
                                    srcDoc=sort_extract_bar_plot(data).to_html()
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col(html.Br())
                        ]),
                        dbc.Row([
                            dbc.Col(html.H3('Price and Rating Analysis'))
                        ]),
                        dbc.Row(
                            dbc.Col(html.Hr(hidden=False,
                                            style={'height':1,
                                                   'background-color': '#50107a',
                                                   'margin-top': 0}))
                        ),
                        dbc.Row([
                            dbc.Col(html.H5('Analyze by Price or Rating'))
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='heatmap_x',
                                    options=[
                                        {'label': 'Rating', 'value': 'points'},
                                        {'label': 'Price', 'value': 'price'},
                                    ],
                                    value='price', 
                                    style=dict(width='45%',
                                            verticalAlign='middle')
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col(html.Br())
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    sandbox='allow-scripts',
                                    id='heatmap_1',
                                    height=600,
                                    width=850,
                                    style={'border-width': '0'},
                                    srcDoc=plot_heatmap(data).to_html()
                                )
                            ])
                        ])
            ])
        ])
])

app.layout = html.Div([jumbotron, 
                       content,
                       html.Div(id='tabs-content-classes')])


@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('bar-chart-x', 'value'),
    dash.dependencies.Input('bar-chart-y', 'value'),
    dash.dependencies.Input('bar-chart-sort', 'value'),
    dash.dependencies.Input('bar-chart-slider', 'value')])
def update_plot(x_name_update, y_name_update, order, obs):
    """
    Takes the x column name and y column name and calls the
    sort_extract_bar_plot() function
    """
    updated_bar_plot = sort_extract_bar_plot(data=data,
                     y_name=y_name_update,
                     x_name=x_name_update,
                     n=obs, direction=order).to_html()
    return updated_bar_plot

@app.callback(
    dash.dependencies.Output('state_choropleth', 'srcDoc'),
    [dash.dependencies.Input('state_id', 'value')])
def update_state_call(state_id):
    """
    Takes the state name from the dropdown list and
    updates the state choropleth chart to that state.
    """
    update_state = plot_choropleth('state', state_id).to_html()
    return update_state

@app.callback(
    dash.dependencies.Output('heatmap_1', 'srcDoc'),
    [dash.dependencies.Input('heatmap_x', 'value')])
def update_heatmap_call(heatmap_x_update):
    """
    Takes the x variable from the dropdown list and
    updates the heatmap according to the user selection.
    """
    update_heatmap = plot_heatmap(data, x_name = heatmap_x_update).to_html()
    return update_heatmap

if __name__ == '__main__':
    app.run_server(debug=True)