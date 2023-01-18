from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

class MultiScatter(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        grouped = df.groupby(['neighbourhood', 'neighbourhood group'])

        # calculate the mean price and number of reviews for each group
        mean_price = grouped['price'].mean().reset_index()
        mean_reviews = grouped['number of reviews'].mean().reset_index()
        mean_service_fee = grouped['service fee'].mean().reset_index()

        # calculate the number of listings per neighbourhood
        listings_per_neighbourhood = grouped.size().reset_index()

        # rename the columns in the new dataframe
        listings_per_neighbourhood.rename(columns={0: 'listings_per_neighbourhood'}, inplace=True)

        # merge the dataframe back to original dataframe
        df = df.merge(mean_price, on=['neighbourhood', 'neighbourhood group'], how='inner')
        df = df.merge(mean_reviews, on=['neighbourhood', 'neighbourhood group'], how='inner')
        df = df.merge(mean_service_fee, on=['neighbourhood', 'neighbourhood group'], how='inner')
        df = df.merge(listings_per_neighbourhood, on=['neighbourhood', 'neighbourhood group'], how='inner')

        # create the scatterplot
        fig = px.scatter(df, x='price_y', y='number of reviews_y', color='neighbourhood group',
                         size='listings_per_neighbourhood', hover_name="neighbourhood", size_max=80,
                         labels={'price_y': 'Average price per night', 'number of reviews_y': 'Average number of reviews'},
                         title='Relationship between Price and Number of Reviews by Neighbourhood and Neighbourhood group')


        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id, figure=fig)
            ],
        )
