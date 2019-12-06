import altair as alt
import pandas as pd
from vega_datasets import data
import sys



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







def wrangle_counties(df):
    """
    Wrangle the data to group by county.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns the data grouped by county in a pandas df.
    """
    # Group and aggregate the data by Counties
    counties_grouped = df.groupby(['county', 'county_id'], as_index=False)
    wine_counties = counties_grouped.agg({'points': ['mean'],
                                          'price': ['mean'],
                                          'value_scaled': ['mean'],
                                          'description': ['count']})

    wine_counties.columns = wine_counties.columns.droplevel(level=1)
    wine_counties = wine_counties.rename(columns={"county": 'County',
                                                  "county_id": 'County ID',
                                                  "description": "Num Reviews",
                                                  "points": 'Ave Points',
                                                  "price": 'Ave Price',
                                                  "value_scaled": 'Ave Value'})

    return wine_counties

def lookup_state_id(df, state_id=6):
    """
    Returns the matched state id based on the input state name.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.
    state -- (str) String of state (ex. 'California')

    Return a Pandas series with the state and state_id
    """
    state = df[['state_id', 'state']].drop_duplicates(keep='first')
    return state.query('state_id == @state_id').iloc[0]

def plot_map(df, state_id=6):
    """
    Plot a Choropleth map of US States and Wine Reviews.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.
    state_id -- (int) Integer of state_id (ex. 6 for 'California)

    Returns altiar plot objects.
    """

    wine_counties = wrangle_counties(df)
    counties = alt.topo_feature(data.us_10m.url, 'counties')

    state = lookup_state_id(df, state_id)
    state_name = state['state']
    state_id = state['state_id']

    colormap = alt.Scale(domain=[0, 100, 500, 1000, 2000, 4000, 8000],
                         range=['#C7DBEA', '#CCCCFF', '#B8AED2', '#3A41C61',
                                '#9980D4', '#4634A7', '#4C2C96'])

    c_foreground = (
        alt.Chart(counties)
        .mark_geoshape(
            stroke='black',
            strokeWidth=1
        ).encode(
            color=alt.Color('Num Reviews:Q',
                            scale=colormap),
            tooltip=[alt.Tooltip('County:O'), 
                     alt.Tooltip('Ave Points:Q', format='.2f'),
                     alt.Tooltip('Ave Price:Q', format='$.2f'),
                     alt.Tooltip('Ave Value:Q', format='.2f'),
                     alt.Tooltip('Num Reviews:Q')]
        )
        .transform_calculate(state_id="(datum.id / 1000)|0")
        .transform_filter((alt.datum.state_id) == state_id)
        .transform_lookup(
            lookup='id',
            from_=alt.LookupData(wine_counties,
                                 'County ID',
                                 ['County', 'County ID', 'Ave Points',
                                  'Ave Price', 'Ave Value', 'Num Reviews']))
    )

    c_background = (
        alt.Chart(counties).mark_geoshape(
            fill='dimgray',
            stroke='gray'
        ).transform_calculate(state_id="(datum.id / 1000)|0")
        .transform_filter((alt.datum.state_id) == state_id)
    ).project(
        'albersUsa'
    )


    return (c_background + c_foreground).configure_view(
                height=400,
                width=240,
                strokeWidth=4,
                fill=None,
                stroke=None)


if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_data.csv', index_col=0)
    plot_map(df)
