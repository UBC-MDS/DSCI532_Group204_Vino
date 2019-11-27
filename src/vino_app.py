import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from vega_datasets import data

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = "V is for Vino"

data = pd.read_csv('../data/cleaned_data.csv', index_col=0)

def sort_extract_bar_plot(data=data, y_name='points', x_name='winery', n=15, direction='desc'):
    """
    Sorts dataframe by column of interest and returns data to
    be entered into altair.
    
    Arguments:
    data -- (dataframe) dataframe to sort
    by -- (str) name of quantitative column to sort by
    col -- (str) name of column of interest
    n -- (int) number of rows to return (default=15)  
    direction -- (str) whether to sort the column by ascending or descending
                       order based on the by column (default='desc')
    """
    def vino_special():
        font = "Candara"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 60, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('vino_special', vino_special)

    # enable the newly registered theme
    alt.themes.enable('vino_special')

    # subset the dataframe
    new_data = data.groupby(x_name)[[y_name]].mean()

    # If we want to sort from highest to lowest:
    if direction == 'desc': 
        new_data = new_data.sort_values(by=y_name, ascending=False).head(n).reset_index()
        ranked_bar = alt.Chart(new_data).mark_bar(color='grey').encode(
            alt.X(x_name +':N',
                      sort=alt.EncodingSortField(
                      field=y_name,  
                      op="sum",  
                      order='descending'  
                  )),
            alt.Y(y_name + ':Q', 
                  scale=alt.Scale(domain=[min(new_data[y_name]),
                     max(new_data[y_name])])
                 ),
            color=alt.condition(
                alt.datum[x_name] == new_data[x_name][0],
                alt.value('red'),
                alt.value('grey')
            )
        ).properties(width=700, height=300) 
        return ranked_bar
    else:
        # If we want to sort from lowest to highest
        new_data = new_data.sort_values(by=y_name, ascending=True).head(n).reset_index()
        ranked_bar = alt.Chart(new_data).mark_bar(color='grey').encode(
            alt.X(x_name +':N',
                      sort=alt.EncodingSortField(
                      field=y_name,  
                      op="sum",  
                      order='ascending'  
                  )),
            alt.Y(y_name + ':Q', 
                  scale=alt.Scale(domain=[min(new_data[y_name])-1,
                             max(new_data[y_name])])
                 ),
            color=alt.condition(
                alt.datum[x_name] == new_data[x_name][0],
                alt.value('red'),
                alt.value('grey')
            )
        ).properties(width=500, height=300) 
        return ranked_bar

app.layout = html.Div([

    html.H1('Main Header'),
    html.H2('Subheader'),
    
    html.H3('Plot 1'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='400',
        width='600',
        style={'border-width': '0'},

        ### Link this Iframe to the dynamic bar plot
        srcDoc=sort_extract_bar_plot().to_html()
    ),
    html.H3('Choose the x axis of the bar plot'),
    dcc.Dropdown(
        id='bar-chart-x',
        options=[
            {'label': 'Winery', 'value': 'winery'},
            {'label': 'Region', 'value': 'region_1'},
            {'label': 'Grape Variety', 'value': 'variety'},
        ],
        value='winery', # not sure what this is doing,
        style=dict(width='45%',
                verticalAlign='middle')
        ),
    dcc.Dropdown(
        id='bar-chart-y',
        options=[
            {'label': 'Rating', 'value': 'points'},
            {'label': 'Price', 'value': 'price'},
            {'label': 'Value', 'value': 'value'},
        ],
        value='points', # may have to change later
        style=dict(width='45%',
                verticalAlign='middle'
        ),
    )
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('bar-chart-x', 'value'),
    dash.dependencies.Input('bar-chart-y', 'value')])
def update_plot(x_name, y_name):
    """
    Takes the x column name and y column name and calls the 
    sort_extract_bar_plot() function
    """
    updated_plot = sort_extract_bar_plot(data, y_name, x_name, n=15, direction='desc')
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)