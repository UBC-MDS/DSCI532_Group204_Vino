import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
# from vega_datasets import data
import states_choropleth
import state_choropleth
from bar_plots import sort_extract_bar_plot

app = dash.Dash(__name__, assets_folder='assets')
server = app.server


app.title = "V is for Vino"

data = pd.read_csv('../data/cleaned_data.csv', index_col=0)

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

app.layout = html.Div([
    dcc.Tabs(
            id="tabs-with-classes",
            value='tab-2',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Tab one',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                        html.Div([
                            html.H1('Choropleth Maps'),
                            html.H3('States Choropleth'),
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='states_choropleth',
                                height='550',
                                width='800',
                                style={'border-width': '0'},

                                ### Link this Iframe to the states choropleth
                                srcDoc=plot_choropleth('states').to_html()
                            ),
                            dcc.Dropdown(
                                id='state_id',
                                options=STATES,
                                value=6, 
                                style=dict(width='45%',
                                        verticalAlign='middle')
                            ),
                            html.H3('State Choropleth'),
                            html.Iframe(
                                sandbox='allow-scripts',
                                id='state_choropleth',
                                height='580',
                                width='800',
                                style={'border-width': '0'},

                                ### Link this Iframe to the dynamic state choropleth
                                srcDoc=plot_choropleth('state').to_html()
                            ),
                    ])]
                ),
                dcc.Tab(
                    label='Tab two',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children = [
                        html.H3('Plot 1'),
                        html.Iframe(
                            sandbox='allow-scripts',
                            id='plot',
                            height='500',
                            width='600',
                            style={'border-width': '0'},
                            ### Link this Iframe to the dynamic bar plot
                            srcDoc=sort_extract_bar_plot(data).to_html()
                        ),
                        html.H3('Choose the x axis of the bar plot'),
                        dcc.Dropdown(
                            id='bar-chart-x',
                            options=[
                                {'label': 'Region', 'value': 'region_1'},
                                {'label': 'Winery', 'value': 'winery'},
                                {'label': 'Grape Variety', 'value': 'variety'},
                            ],
                            value='region_1', # setting default when app loads
                            style=dict(width='45%',
                                    verticalAlign='middle')
                            ),
                        dcc.Dropdown(
                            id='bar-chart-y',
                            options=[
                                {'label': 'Rating', 'value': 'points'},
                                {'label': 'Price', 'value': 'price'},
                                {'label': 'Value', 'value': 'value_scaled'},
                            ],
                            value='points',
                            style=dict(width='45%',
                                    verticalAlign='middle')
                            ),
                        dcc.RadioItems(
                            id='bar-chart-sort',
                            options=[
                                {'label': 'Lowest to Highest', 'value': 'asc'},
                                {'label': 'Highest to Lowest', 'value': 'desc'}
                            ],
                            value='asc'
                        ),
                    ]
                )
     ]),
        html.Div(id='tabs-content-classes')
])


@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('bar-chart-x', 'value'),
    dash.dependencies.Input('bar-chart-y', 'value'),
    dash.dependencies.Input('bar-chart-sort', 'value')])
def update_plot(x_name_update, y_name_update, order):
    """
    Takes the x column name and y column name and calls the
    sort_extract_bar_plot() function
    """
    updated_bar_plot = sort_extract_bar_plot(data=data,
                     y_name=y_name_update,
                     x_name=x_name_update,
                     n=15, direction=order).to_html()
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


if __name__ == '__main__':
    app.run_server(debug=True)