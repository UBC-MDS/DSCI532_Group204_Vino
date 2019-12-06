import altair as alt
import pandas as pd
from vega_datasets import data


def vino_special():
    font = "Helvetica"
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
                "labelAngle": 60, 
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
                "labelAngle": 0, 
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



def wrangle_states(df):
    """
    Wrangle the data to group by state.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns the data grouped by state in a pandas df.
    """
    # Group and aggregate the data by States
    states_grouped = df.groupby(['state', 'state_id'], as_index=False)
    wine_states = states_grouped.agg({'points': ['mean'],
                                      'price': ['mean'],
                                      'value_scaled': ['mean'],
                                      'description': ['count']})

    wine_states.columns = wine_states.columns.droplevel(level=1)
    wine_states = wine_states.rename(columns={"state": "State",
                                              "state_id": "State ID",
                                              "description": "Num Reviews",
                                              "points": 'Ave Points',
                                              "price": 'Ave Price',
                                              "value_scaled": 'Ave Value'})
    return wine_states


def plot_map(df):
    """
    Plot a Choropleth map of US States and Wine Reviews.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns altiar plot objects.
    """


    wine_states = wrangle_states(df)
    states = alt.topo_feature(data.us_10m.url, "states")

    colormap = alt.Scale(domain=[0, 100, 1000, 2000, 4000, 8000, 16000, 32000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#722CB7', '#663399', '#512888'])

    foreground = alt.Chart(states).mark_geoshape().encode(
        color=alt.Color('Num Reviews:Q',
                        scale=colormap),
        tooltip=[alt.Tooltip('State:O'),
                 alt.Tooltip('Ave Points:Q', format='.2f'),
                 alt.Tooltip('Ave Price:Q', format='$.2f'),
                 alt.Tooltip('Ave Value:Q', format='.2f'),
                 alt.Tooltip('Num Reviews:Q')]
    ).mark_geoshape(
        stroke='black',
        strokeWidth=0.5
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(wine_states,
                             'State ID',
                             ['State', 'State ID', 'Ave Points', 'Ave Price', 'Ave Value', 'Num Reviews'])
    ).project(
        type='albersUsa'
    )

    background = alt.Chart(states).mark_geoshape(
        fill='gray',
        stroke='dimgray'
    ).project(
        'albersUsa'
    )
    
    return (background + foreground).configure_view(
                height=400,
                width=570,
                strokeWidth=4,
                fill=None,
                stroke=None)


if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_data.csv', index_col=0)
    plot_map(df)
	