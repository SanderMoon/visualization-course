from dash import dcc, html
import plotly.graph_objects as go


class Splom(html.Div):
    def __init__(self, name, features, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.features = features

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
    
    def update(self, selected_color, selected_data):
      index_vals = self.df['species'].astype('category').cat.codes
      self.fig = go.Figure()

      self.fig.add_trace(go.Splom(dimensions=[dict(label="sepal_width", values=self.df["sepal_width"]),
                                              dict(label="sepal_length", values=self.df["sepal_length"]),
                                              dict(label="petal_width", values=self.df["petal_width"]),
                                              dict(label="petal_length", values=self.df["petal_length"])],
      
                                  marker=dict(color=index_vals,
                                              showscale=False, # colors encode categorical variables
                                              line_color='white', line_width=0.5),
                                  showupperhalf=False
                                              ))

      # highlight points with selection other graph
      if selected_data is None:
          selected_index = self.df.index  # show all
      else:
          selected_index = [  # show only selected indices
              x.get('pointIndex', None)
              for x in selected_data['points']
          ]

      self.fig.data[0].update(
          selectedpoints=selected_index,

          # color of selected points
          selected=dict(marker=dict(color=selected_color)),

          # color of unselected pts
          unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
      )
                                            
      self.fig.update_layout(
        title='Iris Data set',
        width=1000,
        height=1000,
        yaxis_zeroline=False,
        xaxis_zeroline=False,
        dragmode='select'
      )

      return self.fig