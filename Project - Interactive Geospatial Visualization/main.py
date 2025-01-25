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


# Callback to create and update the dashboard based on user interactions
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
def update_dashboard(map_click_data, tree_click_data, last_clicked_state, last_clicked_airport):
    """
    Update the dashboard based on user interactions.
    :param map_click_data: Click data from the map.
    :param tree_click_data: Click data from the treemap.
    :param last_clicked_state: The last clicked state.
    :param last_clicked_airport: The last clicked airport.
    :return: Updated figures based on chosen states and airports.
    """
    # Default clicked values
    clicked_state = last_clicked_state
    clicked_airport = last_clicked_airport

    # Create the initial figures
    map_fig = create_choropleth(map_data, airport_data)

    tree_fig = px.treemap(
        tree_data, color='Total Flights per state', values='Flights',
        path=['StateCode', 'Origin', 'Reporting_Airline'],
        color_continuous_scale='YlOrRd',
        title='Flights distribution across airports in the US'
    )

    sunburst_fig = px.sunburst(
        sunburst_data, values="Flights", color="Status",
        path=["Reporting_Airline", "Status", "Detail"],
        color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
        title="Airlines performances in the US",
    )

    line_fig = px.line(
        line_data, x='Month', y='AirTime', color='Reporting_Airline',
        title='Average Monthly Flight Time per airline in the US'
    )

    # Determine which input triggered the callback
    ctx = dash.callback_context

    if ctx.triggered:
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        # If the map was clicked
        if trigger == "plot2" and map_click_data:

            # Extract the clicked state
            clicked_state = map_click_data["points"][0]["location"]
            state_name = map_data[map_data['StateCode'] == clicked_state]['StateName'].values[0]

            # Check if the clicked state is different from the last clicked state
            if clicked_state != last_clicked_state:
                # Update the figures
                map_fig = create_choropleth(map_data, airport_data, selected_state=clicked_state, zoom_level=4)

                tree_fig = px.treemap(
                    tree_data[tree_data['StateCode'] == clicked_state],
                    color='Total Flights per state', values='Flights',
                    path=['StateCode', 'Origin', 'Reporting_Airline'], color_continuous_scale='YlOrRd',
                    title=f'Flights distribution across airports in {state_name}, US'
                )

                sunburst_fig = px.sunburst(
                    sunburst_data[sunburst_data['StateCode'] == clicked_state], color="Status", values="Flights",
                    path=["Reporting_Airline", "Status", "Detail"],
                    color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
                    title=f'Airlines performances in {state_name}, US'
                )

                line_fig = px.line(
                    line_data[line_data['StateCode'] == clicked_state], x='Month', y='AirTime',
                    color='Reporting_Airline', title=f'Average Monthly Flight Time per airline in {state_name}, US'
                )

        # If the treemap was clicked
        elif trigger == "plot1" and tree_click_data:

            # Extract the clicked state and airport
            clicked_state = tree_click_data["points"][0]["parent"]
            clicked_airport = tree_click_data["points"][0]["label"]

            # Extract the state name
            state_name = tree_data[tree_data['StateCode'] == clicked_state]['StateName'].values[0]

            # Check if the clicked airport is different from the last clicked airport
            if clicked_airport != last_clicked_airport:
                # Update the figures
                map_fig = create_choropleth(map_data, airport_data, selected_state=clicked_state, zoom_level=4)

                tree_fig = px.treemap(
                    tree_data[tree_data['Origin'] == clicked_airport],
                    color='Total Flights per state', values='Flights',
                    path=['StateCode', 'Origin', 'Reporting_Airline'], color_continuous_scale='YlOrRd',
                    title=f'Flights distribution per airline at the {clicked_airport} airport in {state_name}, US'
                )

                sunburst_fig = px.sunburst(
                    sunburst_data[sunburst_data['Origin'] == clicked_airport], color="Status", values="Flights",
                    path=["Reporting_Airline", "Status", "Detail"],
                    color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
                    title=f'Airlines performances at the {clicked_airport} airport in {state_name}, US',
                )

                line_fig = px.line(
                    line_data[line_data['Origin'] == clicked_airport], x='Month', y='AirTime',
                    color='Reporting_Airline',
                    title=f'Average Monthly Flight Time per airline at {clicked_airport} airport in {state_name}, US'
                )

    # Adjust layouts
    map_fig.update_layout(geo_scope='usa', autosize=True)

    tree_fig.update_layout(autosize=True, margin=dict(l=20, r=0, t=80, b=20))

    sunburst_fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=80, b=50))

    line_fig.update_layout(autosize=True)

    # Return updated figures and clicked values
    return [
        tree_fig,
        map_fig,
        sunburst_fig,
        line_fig,
        clicked_state,
        clicked_airport
    ]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
