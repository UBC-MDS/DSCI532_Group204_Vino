import altair as alt
import pandas as pd
from vega_datasets import data
from vino_special import vino_special

def wrangle_varieties(df):
    """
    Wrangle the data to group by state.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns the data grouped by va
    """

    # Group and aggregate data by wine varieties
    variety_df = df.groupby(['variety']).size().reset_index(name='counts')
    variety_df = variety_df.sort_values(by='counts')
    popular_varieties = variety_df.query('counts > 500')['variety']

    # Filter the data set to include only popular grape varieties
    varieties_plot_data = df[df['variety'].isin(popular_varieties.tolist())]

    return varieties_plot_data


def plot_heatmap(df, x_name='price'):
    """
    Plot a heatmap of showing the average value of wines from popular grape varieties at a range of price points.

    Parameters:
    -----------
    df -- (pandas DataFrame) Cleaned data in a dataframe.

    Returns altiar plot objects.
    """

    varieties_chart_data = wrangle_varieties(df)

    if x_name == 'price': 
        varieties_heatmap_plot = alt.Chart(varieties_chart_data.query('price < 50')).mark_rect().encode(
            x=alt.X(x_name + ':Q',
                    bin=alt.Bin(maxbins=10),
                    title="Price"),
            y=alt.Y('variety:O', 
                    title="Grape Variety"),
            color=alt.Color('average(value_scaled):Q',
                            scale=alt.Scale(scheme="bluepurple"),
            legend=alt.Legend(
                            orient='right', title="Average Value")
                        ),
            tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                     alt.Tooltip('average(price)', format='$.2f'),
                     alt.Tooltip('average(value_scaled)', format='.2f'),
                     alt.Tooltip('count(title)')]
        ).properties(
            title="Average Value for Grape Varieties by Price"
        ).configure_axis(
            grid=False
        )
    
    if x_name == 'points':
        varieties_heatmap_plot = alt.Chart(varieties_chart_data).mark_rect().encode(
            x=alt.X('points:Q',
                        bin=alt.Bin(maxbins=10),
                        title="Rating"),
            y=alt.Y('variety:O', 
                    title="Grape Variety"),
            color=alt.Color('average(value_scaled):Q',
                            scale=alt.Scale(scheme="bluepurple"),
            legend=alt.Legend(
                            orient='right', title="Average Value")
                        ),
            tooltip=[alt.Tooltip('average(points):Q', format='.2f'),
                     alt.Tooltip('average(price)', format='$.2f'),
                     alt.Tooltip('average(value_scaled)', format='.2f'),
                     alt.Tooltip('count(title)')]
        ).properties(
            title="Average Value for Grape Varieties by Rating"
        ).configure_axis(
            grid=False
        )
    
    return varieties_heatmap_plot


if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_data.csv', index_col=0)
    plot_heatmap(df)