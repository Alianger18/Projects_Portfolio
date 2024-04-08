# Import the required libraries
from helping_functions import fetch_data
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlite3
import dash

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div(style={'font-family': 'Arial, sans-serif'},
                      children=[html.Header(
                          style={'background-color': '#05668D',
                                 'color': '#ebf2fa',
                                 'padding': '10px',
                                 'text-align': 'center'
                                 },
                          children=[
                              html.H1("Manufacturing Dashboard")
                          ]
                      ),
                          html.Div(className="content",
                                   style={'display': 'flex', 'width': '100%'},
                                   children=[
                                       html.Div(className="plot-container",
                                                style={'flex': '1', 'padding': '20px'},
                                                children=[dcc.Graph(id='line-plot', style={'width': '100%',
                                                                                           'height': '650px'})]
                                                ),
                                       html.Div(className="table-container",
                                                style={'flex': '1', 'padding': '15px', 'text-align': 'center'},
                                                children=[
                                                    html.H2("Collected Measurements and Predicted Score"),
                                                    dash_table.DataTable(
                                                        id="data-table",
                                                        columns=[
                                                            {"name": "Timestamp", "id": "timestamp"},
                                                            {"name": "Sound", "id": "sound"},
                                                            {"name": "Temperature", "id": "temperature"},
                                                            {"name": "Humidity", "id": "humidity"},
                                                            {"name": "Score", "id": "score"}
                                                        ],
                                                        style_header={
                                                            'backgroundColor': '#05668D',
                                                            'color': '#ebf2fa',
                                                            'font-family': 'Arial, sans-serif',
                                                            'text-align': 'center',
                                                            'fontWeight': 'bold'
                                                        },
                                                        style_cell={
                                                            'font-family': 'Arial, sans-serif',
                                                            'text-align': 'center',
                                                            'backgroundColor': '#f2f2f2',
                                                            'color': '#000000'
                                                        },
                                                        style_table={
                                                            'overflowX': 'auto',
                                                            'margin': 'auto'
                                                        },
                                                        page_size=30,  # Adjust as needed
                                                    )
                                                ])
                                   ]
                                   ),
                          html.Footer(style={'background-color': '#05668D', 'color': '#ebf2fa', 'padding': '10px',
                                             'text-align': 'center', 'margin-top': 'auto'},
                                      children=[html.P([html.Strong("Wind"), ". Means the world to us."]),
                                                html.P(["© 2024 ", html.Strong("VESTAS"), ".Inc"])
                                                ]),
                          dcc.Interval(id='interval-component',
                                       interval=5000,  # in milliseconds
                                       n_intervals=0
                                       )
                      ]
                      )


# Define callback to update data and plot
@app.callback(
    [Output('data-table', 'data'),
     Output('line-plot', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_data_and_plot(n_intervals):
    # Connect to the SQLite database
    with sqlite3.connect("main.db") as conn:
        # Fetch data from database
        df = fetch_data(connection=conn)

    # Create line plot with custom color scale and color bands
    line_plot = go.Figure()

    # Add line trace
    line_plot.add_trace(go.Scatter(x=df['timestamp'], y=df['score'], mode='lines', name='Score'))

    # Define score levels and corresponding colors
    score_levels = [0, 1, 3, 5, 7, 10]
    colors = ['darkred', 'red', 'yellow', 'orange', 'green']

    # Add color bands
    for i in range(len(score_levels) - 1):
        line_plot.add_shape(
            type="rect",
            xref="paper",
            yref="y",
            x0=0,
            x1=1,
            y0=score_levels[i],
            y1=score_levels[i+1],
            fillcolor=colors[i],
            opacity=0.5,
            layer="below",
            line=dict(width=0),
        )

    # Customize layout of the plot
    line_plot.update_layout(
        title=dict(
            text='Score Variation Over Time',  # Set plot title
            font=dict(
                family='Arial, sans-serif',  # Set font family
                size=20,  # Set font size
                color='black'
            )
        ),  # Set plot title
        xaxis_title='Timestamp',  # Set title for x-axis
        yaxis_title='Score',  # Set title for y-axis
        xaxis=dict(
            showgrid=False,  # Show gridlines on x-axis
            zeroline=False,  # Hide the zero line
        ),
        yaxis=dict(
            showgrid=False,  # Show gridlines on y-axis
            zeroline=False,  # Hide the zero line
        ),
        plot_bgcolor='white',  # Set background color of the plot
        paper_bgcolor='white',  # Set background color of the paper
        font=dict(family='Arial, sans-serif', size=12, color='black'),  # Set font family, size, and color
        margin=dict(l=50, r=50, t=50, b=50),  # Set margins
    )

    return df.to_dict('records'), line_plot


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
