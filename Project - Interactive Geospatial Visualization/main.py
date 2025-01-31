# Import the required libraries
from dash.dependencies import Input, Output, State
from dash import dcc, html, Dash
from functions import *
from pathlib import Path
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
        dcc.Store(id="last-clicked-airport", data=None),
        dcc.Store(id="last-clicked-airline", data=None)
    ]
)


@app.callback(
    [
        Output("plot1", "figure"),                  # Update the treemap
        Output("plot2", "figure"),                  # Update the map
        Output("plot3", "figure"),                  # Update the sunburst
        Output("plot4", "figure"),                  # Update the line chart
        Output("last-clicked-state", "data"),       # Store clicked state
        Output("last-clicked-airport", "data"),     # Store clicked airport
        Output("last-clicked-airline", "data")      # Store clicked airline
    ],
    [
        Input("plot2", "clickData"),                # Clicks on the map
        Input("plot1", "clickData"),                # Clicks on the treemap
        Input("plot3", "clickData")                 # Clicks on the sunburst
    ],
    [
        State("last-clicked-state", "data"),        # Previous clicked state
        State("last-clicked-airport", "data"),      # Previous clicked airport
        State("last-clicked-airline", "data")       # Previous clicked airline
    ]
)
def update_dashboard(map_click_data,
                     tree_click_data,
                     sunburst_click_data,
                     last_clicked_state,
                     last_clicked_airport,
                     last_clicked_airline):
    """
    Update the dashboard based on user interactions
    :param map_click_data: Click data from the map
    :param tree_click_data: Click data from the treemap
    :param sunburst_click_data: Click data from the sunburst
    :param last_clicked_state: Last clicked state
    :param last_clicked_airport: Last clicked airport
    :param last_clicked_airline: Last clicked airline
    :return: Custom figures based on the user preferences
    """
    # Default clicked values
    clicked_state = last_clicked_state
    clicked_airport = last_clicked_airport
    clicked_airline = last_clicked_airline

    # Create the initial figures
    map_fig = create_choropleth(map_data, airport_data)

    tree_fig = create_tree_map(tree_data)

    sunburst_fig = create_sunburst(sunburst_data)

    line_fig = create_line(line_data)

    # Determine which input triggered the callback
    ctx = dash.callback_context

    # If the callback was triggered
    if ctx.triggered:

        #
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        # If the map was clicked
        if trigger == "plot2" and map_click_data:

            # Get the clicked state
            clicked_state = map_click_data["points"][0]["location"]

            # Update only the figures if the clicked state is different from the last clicked state
            if clicked_state != last_clicked_state:

                # Update all figures with the clicked state
                map_fig = create_choropleth(map_data, airport_data, selected_state=clicked_state, zoom_level=4)

                tree_fig = create_tree_map(tree_data, clicked_state)

                sunburst_fig = create_sunburst(sunburst_data, clicked_state)

                line_fig = create_line(line_data, clicked_state)

            else:

                # Return to the initial state
                map_fig = create_choropleth(map_data, airport_data)

                tree_fig = create_tree_map(tree_data)

                sunburst_fig = create_sunburst(sunburst_data)

                line_fig = create_line(line_data)

        # If the treemap was clicked
        elif trigger == "plot1" and tree_click_data:

            # Get the clicked airport, state code and name
            clicked_state = tree_click_data["points"][0]["parent"]
            clicked_airport = tree_click_data["points"][0]["label"]

            # Update the map with the clicked state
            map_fig = create_choropleth(map_data, airport_data, selected_state=clicked_state, zoom_level=4)

            # Update only the figures if the clicked airport is different from the last clicked airport
            if clicked_airport != last_clicked_airport:

                # Update all figures with the clicked airport
                tree_fig = create_tree_map(tree_data, clicked_state, clicked_airport)

                sunburst_fig = create_sunburst(sunburst_data, clicked_state, clicked_airport)

                line_fig = create_line(line_data, clicked_state, clicked_airport)

            else:
                # Return to the initial state
                tree_fig = create_tree_map(tree_data, clicked_state)

                sunburst_fig = create_sunburst(sunburst_data, clicked_state)

                line_fig = create_line(line_data, clicked_state)

        # If the sunburst was clicked
        elif trigger == "plot3" and sunburst_click_data:

            # Determine the clicked airline
            clicked_airline = sunburst_click_data["points"][0]["label"]

            # Update the map with the last clicked state
            map_fig = create_choropleth(map_data, airport_data, selected_state=last_clicked_state, zoom_level=4)

            tree_fig = create_tree_map(tree_data, clicked_state, clicked_airport)

            # Update only the figures if the clicked airline is different from the last clicked airline
            if clicked_airline != last_clicked_airline or clicked_airline is None:

                # Update all figures with the clicked airline
                sunburst_fig = create_sunburst(sunburst_data, clicked_state, clicked_airport, clicked_airline)

                line_fig = create_line(line_data, clicked_state, clicked_airport, clicked_airline)

            else:
                # Return to the initial state
                sunburst_fig = create_sunburst(sunburst_data, clicked_state, clicked_airport)

                line_fig = create_line(line_data, clicked_state, clicked_airport)

    # Adjust layouts
    map_fig.update_layout(geo_scope='usa', autosize=True)
    tree_fig.update_layout(autosize=True, margin=dict(l=20, r=0, t=80, b=20))
    sunburst_fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=80, b=50))
    line_fig.update_layout(autosize=True)

    # Return the results
    return [
        tree_fig,
        map_fig,
        sunburst_fig,
        line_fig,
        clicked_state,
        clicked_airport,
        clicked_airline
    ]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
