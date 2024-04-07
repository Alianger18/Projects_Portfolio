import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'font-family': 'Arial, sans-serif'}, children=[
    html.Header(style={'margin': '0', 'background-color': '#05668D', 'color': '#ebf2fa', 'padding': '10px', 'text-align': 'center', 'width': '100%'}, children=[
        html.H1("Manufacturing Dashboard")
    ]),
    html.Div(className="content", style={'display': 'flex', 'flex-direction': 'row', 'flex': '1', 'width': '100%'}, children=[
        html.Div(className="plot-container", style={'flex': '1', 'padding': '20px'}, children=[
            html.Iframe(src="plotly_graph.html", width="100%", height="700px", style={'background-color': '#7ea0c5', 'border': '1px solid #1d3461', 'border-radius': '5px', 'width': '100%'})
        ]),
        html.Div(className="table-container", style={'flex': '1', 'padding': '15px'}, children=[
            html.H2("Collected Measurements and Predicted Score"),
            html.Table(id="data-table", children=[
                html.Thead(html.Tr([
                    html.Th("Timestamp", style={'background-color': '#05668D', 'color': '#ebf2fa'}),
                    html.Th("Sound", style={'background-color': '#05668D', 'color': '#ebf2fa'}),
                    html.Th("Temperature", style={'background-color': '#05668D', 'color': '#ebf2fa'}),
                    html.Th("Humidity", style={'background-color': '#05668D', 'color': '#ebf2fa'}),
                    html.Th("Score", style={'background-color': '#05668D', 'color': '#ebf2fa'})
                ])),
                html.Tbody(id="table-body", children=[
                    # Data will be dynamically inserted here
                ])
            ])
        ])
    ]),
    html.Footer(style={'margin': '-1', 'background-color': '#05668D', 'color': '#ebf2fa', 'padding': '10px', 'text-align': 'center', 'width': '100%'}, children=[
        html.P([html.Strong("Wind"), ". Means the world to us."]),
        html.P(["© 2024 ", html.Strong("VESTAS"), ".Inc"])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  # Change the port number as needed
