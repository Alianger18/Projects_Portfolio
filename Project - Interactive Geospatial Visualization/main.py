# Import the required libraries
from dash.dependencies import Input, Output, State
from functions import create_choropleth
from dash import dcc, html, Dash
from pathlib import Path
import plotly.express as px
import pandas as pd
import dash

# Get the current working directory
path = Path.cwd()

# Load the data
airport_data = pd.read_csv(f"{path}/data/airport_data.csv")
map_data = pd.read_csv(f"{path}/data/map_data.csv")
tree_data = pd.read_csv(f"{path}/data/tree_data.csv")
sunburst_data = pd.read_csv(f"{path}/data/sunburst_data.csv")
line_data = pd.read_csv(f"{path}/data/line_data.csv")

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={
        'margin': '0',
        'font-family': 'Arial, sans-serif',
        'background-color': '#B3B3B3FF',
        'padding': '0',
        'width': '100%',
        'height': '100%',
        'box-sizing': 'border-box'
    },
    children=[
        # Title Section
        html.Div(
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'padding': '20px',
                'max-width': '1920px',
                'margin': '0',
                'margin-bottom': '20px'
            },
            children=html.H1(
                "US Domestic Airline Dashboard",
                style={
                    'font-size': '36px',
                    'margin': '0',
                    'text-align': 'center',
                    'color': '#000'
                }
            )
        ),

        # Upper Graphs Section
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'space-between',
                'padding': '0 20px',
                'margin-bottom': '20px'
            },
            children=[
                # Treemap Chart
                dcc.Graph(
                    id="plot1",
                    style={
                        'background-color': '#ffffff',
                        'width': '33%',
                        'height': '70vh',
                        'border-radius': '10px',
                        'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
                    }
                ),

                # Map Chart
                dcc.Graph(
                    id="plot2",
                    style={
                        'background-color': '#ffffff',
                        'width': '66%',
                        'height': '70vh',
                        'border-radius': '10px',
                        'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
                    }
                )
            ]
        ),

        # Bottom Graphs Section
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'space-between',
                'padding': '0 20px',
                'margin-bottom': '20px'
            },
            children=[
                # Sunburst Chart
                dcc.Graph(
                    id="plot3",
                    style={
                        'background-color': '#ffffff',
                        'width': '33%',
                        'height': '50vh',
                        'border-radius': '10px',
                        'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
                    }
                ),

                # Line Chart
                dcc.Graph(
                    id="plot4",
                    style={
                        'background-color': '#ffffff',
                        'width': '66%',
                        'height': '50vh',
                        'border-radius': '10px',
                        'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
                    }
                )
            ]
        ),

        # Footer Section
        html.Div(
            style={
                'background-color': '#333',
                'color': '#fff',
                'padding': '10px 20px',
                'text-align': 'center',
                'font-size': '14px',
                'border-top': '2px solid #555'
            },
            children="© 2025 US Domestic Airline Dashboard. All rights reserved."
        ),

        # Stores for Clicked Data
        dcc.Store(id="last-clicked-state", data=None),
        dcc.Store(id="last-clicked-airport", data=None)
    ]
)


@app.callback(
    [
        Output("plot1", "figure"),  # Update the treemap
        Output("plot2", "figure"),  # Update the map
        Output("plot3", "figure"),  # Update the sunburst
        Output("plot4", "figure"),  # Update the line chart
        Output("last-clicked-state", "data"),  # Store clicked state
        Output("last-clicked-airport", "data")  # Store clicked airport
    ],
    [
        Input("plot2", "clickData"),  # Clicks on the map
        Input("plot1", "clickData")  # Clicks on the treemap
    ],
    [
        State("last-clicked-state", "data"),  # Previous clicked state
        State("last-clicked-airport", "data")  # Previous clicked airport
    ]
)
def update_dashboard(map_click_data,
                     tree_click_data,
                     last_clicked_state,
                     last_clicked_airport,
                     ):
    """
    Update the dashboard based on user interactions.
    """

    # Default clicked values
    clicked_state = last_clicked_state
    clicked_airport = last_clicked_airport

    # Create Initial figures
    map_fig = create_choropleth(map_data, airport_data)

    tree_fig = px.treemap(
        tree_data,
        color='Flights',
        values='Flights',
        title='Filtered Treemap',
        path=['StateCode', 'Origin', 'Reporting_Airline'],
        color_continuous_scale='GnBu')

    sunburst_fig = px.sunburst(
        sunburst_data,
        path=["Reporting_Airline", "Status", "Detail"],
        color="Status",
        values="Flights",
        title="Filtered Sunburst",
        color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"})

    line_fig = px.line(
        line_data,
        x='Month',
        y='AirTime',
        color='Reporting_Airline',
        title='Average Monthly Flight Time'
    )

    # Determine which input triggered the callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Check which input triggered the callback
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        # Extract clicked values from map
        if trigger == "plot2" and map_click_data:

            # Extract state
            clicked_state = map_click_data["points"][0]["location"]  # Extract state from map

            #
            if clicked_state != last_clicked_state:

                # Generate Charts accordingly
                map_fig = create_choropleth(map_data,
                                            airport_data,
                                            selected_state=clicked_state,
                                            zoom_level=4)

                tree_fig = px.treemap(tree_data[tree_data['StateCode'] == clicked_state],
                                      path=['StateCode', 'Origin', 'Reporting_Airline'],
                                      values='Flights',
                                      color='Flights',
                                      title='Treemap',
                                      color_continuous_scale='GnBu')

                sunburst_fig = px.sunburst(sunburst_data[sunburst_data['StateCode'] == clicked_state],
                                           path=["Reporting_Airline", "Status", "Detail"],
                                           color="Status",
                                           values="Flights",
                                           title="Sunburst",
                                           color_discrete_map={"Cancelled": "red",
                                                               "Delayed": "orange",
                                                               "On-Time": "green"
                                                               }
                                           )

                line_fig = px.line(line_data[line_data['StateCode'] == clicked_state],
                                   x='Month',
                                   y='AirTime',
                                   color='Reporting_Airline',
                                   title='Monthly Flight Time')

        # Extract clicked values from treemap
        elif trigger == "plot1" and tree_click_data:

            #
            clicked_state = tree_click_data["points"][0]["parent"]  # Extract state from treemap
            clicked_airport = tree_click_data["points"][0]["label"]

            if clicked_airport != last_clicked_airport:
                # Generate Charts accordingly
                map_fig = create_choropleth(map_data,
                                            airport_data,
                                            selected_state=clicked_state,
                                            zoom_level=4)

                tree_fig = px.treemap(tree_data[tree_data['Origin'] == clicked_airport],
                                      path=['StateCode', 'Origin', 'Reporting_Airline'],
                                      values='Flights',
                                      color='Flights',
                                      title='Treemap',
                                      color_continuous_scale='GnBu')

                sunburst_fig = px.sunburst(sunburst_data[sunburst_data['Origin'] == clicked_airport],
                                           path=["Reporting_Airline", "Status", "Detail"],
                                           color="Status",
                                           values="Flights",
                                           title="Sunburst",
                                           color_discrete_map={"Cancelled": "red",
                                                               "Delayed": "orange",
                                                               "On-Time": "green"
                                                               }
                                           )

                line_fig = px.line(line_data[line_data['Origin'] == clicked_airport],
                                   x='Month',
                                   y='AirTime',
                                   color='Reporting_Airline',
                                   title='Monthly Flight Time')
            else:
                # Generate Charts accordingly
                map_fig = create_choropleth(map_data,
                                            airport_data,
                                            selected_state=clicked_state,
                                            zoom_level=4)

                tree_fig = px.treemap(tree_data[tree_data['StateCode'] == clicked_state],
                                      path=['StateCode', 'Origin', 'Reporting_Airline'],
                                      values='Flights',
                                      color='Flights',
                                      title='Treemap',
                                      color_continuous_scale='GnBu')

                sunburst_fig = px.sunburst(sunburst_data[sunburst_data['StateCode'] == clicked_state],
                                           path=["Reporting_Airline", "Status", "Detail"],
                                           color="Status",
                                           values="Flights",
                                           title="Sunburst",
                                           color_discrete_map={"Cancelled": "red",
                                                               "Delayed": "orange",
                                                               "On-Time": "green"
                                                               }
                                           )

                line_fig = px.line(line_data[line_data['StateCode'] == clicked_state],
                                   x='Month',
                                   y='AirTime',
                                   color='Reporting_Airline',
                                   title='Monthly Flight Time')

    # Adjust layouts
    map_fig.update_layout(geo_scope='usa', autosize=True)
    tree_fig.update_layout(autosize=True)
    sunburst_fig.update_layout(autosize=True, margin=dict(t=10, l=10, r=10, b=10))
    line_fig.update_layout(autosize=True)

    # Return updated figures and clicked values
    return [
        tree_fig,
        map_fig,
        sunburst_fig,
        line_fig,
        clicked_state,
        clicked_airport,
    ]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
