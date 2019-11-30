import altair as alt
import pandas as pd

x_labels = {'region_1': 'Region',
            'winery': 'Winery',
            'variety': 'Grape Variety'}

y_labels = {'points': 'Rating',
            'price': 'Price',
            'value_scaled': 'Value'}

def sort_extract_bar_plot(data, y_name='points', x_name='winery', n=15, direction='desc'):
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
                    "width": 500
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

    # subset the dataframe
    new_data = data.groupby(x_name)[[y_name]].mean()

    # If we want to sort from highest to lowest:
    if direction == 'desc': 
        new_data = new_data.sort_values(by=y_name, ascending=False).head(n).reset_index()
        ranked_bar = alt.Chart(new_data).mark_bar().encode(
            alt.X(x_name +':N',
                      sort=alt.EncodingSortField(
                      field=y_name,  
                      op="sum",  
                      order='descending',  
                  )),
            alt.Y(y_name + ':Q', title=y_labels[y_name],
                  scale=alt.Scale(domain=[min(new_data[y_name]),
                     max(new_data[y_name])])
                 ),
            color=alt.condition(
                alt.datum[x_name] == new_data[x_name][0],
                alt.value('#512888'),
                alt.value('lightgrey')
            ),
            tooltip=[alt.Tooltip(f'{x_name}:N'),
                    alt.Tooltip(f'{y_name}:Q')]
        ).properties(width=500, height=300, title='Average ' + y_labels[y_name] + ' by ' + x_labels[x_name]) 
        return ranked_bar
    else:
        # If we want to sort from lowest to highest
        new_data = new_data.sort_values(by=y_name, ascending=True).head(n).reset_index()
        ranked_bar = alt.Chart(new_data).mark_bar().encode(
            alt.X(x_name +':N',
                      sort=alt.EncodingSortField(
                      field=y_name,  
                      op="sum",  
                      order='ascending'  
                  )),
            alt.Y(y_name + ':Q', title=y_labels[y_name], 
                  scale=alt.Scale(domain=[min(new_data[y_name])-1,
                             max(new_data[y_name])])
                 ),
            color=alt.condition(
                alt.datum[x_name] == new_data[x_name][0],
                alt.value('#512888'),
                alt.value('lightgrey')
            ),
            tooltip=[x_name + ':N', y_name + ':Q']
        ).properties(width=500, height=300, title='Average ' + y_labels[y_name] + ' by ' + x_labels[x_name]) 
        return ranked_bar