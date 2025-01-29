# Importing the required libraries
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

# Get the current working directory
path = Path.cwd()

# Load the data
airport_coords_df = pd.read_csv(f"{path}/data/airports_coordinates.csv")
states_coords_df = pd.read_csv(f"{path}/data/us_state_coordinates.csv")


# Defining the functions
def get_airports_data(dataframe: pd.DataFrame):
    """
    Get the airports data from the given dataframe.

    Arguments:
    dataframe: Filtered dataframe.

    Returns:
    Dataframe containing the airport data.
    """
    # Aggregate airport-level data
    airport_flights = dataframe.groupby('Origin')['Flights'].sum().reset_index()
    airport_flights.rename(columns={'Origin': 'AirportCode'}, inplace=True)
    airport_data = pd.merge(airport_coords_df, airport_flights, on='AirportCode', how='left')
    airport_data['Flights'] = airport_data['Flights'].fillna(0)
    airport_data['Flights'] = airport_data['Flights'].astype(int)
    airport_data.sort_values('StateName', ascending=True, inplace=True)

    # Return the results
    return airport_data

def get_map_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the map data for the given dataframe.

    Arguments:
    dataframe: Filtered dataframe.

    Returns:
    Dataframe containing the map data.
    """
    # Group data by state
    map_data = dataframe.groupby(['OriginState', 'OriginStateName'])['Flights'].sum().reset_index()

    # Fill missing values
    map_data['Flights'] = map_data['Flights'].fillna(0)

    # Convert the flights to integers
    map_data['Flights'] = map_data['Flights'].astype(int)

    # Rename the columns
    map_data.rename(columns={'OriginState': 'StateCode', 'OriginStateName': 'StateName'}, inplace=True)

    # Sort the data
    map_data.sort_values('StateName', ascending=True, inplace=True)

    # Return the results
    return map_data

def get_tree_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the tree data for the given dataframe.

    Arguments:
    dataframe: Filtered dataframe.

    Returns:
    Dataframe containing the tree data.
    """
    # Group data by state, airport, and airline
    tree_data = dataframe.groupby(
        ['OriginState', 'OriginStateName', 'Origin', 'Reporting_Airline']
    )['Flights'].sum().reset_index()

    # Fill missing values
    tree_data['Flights'] = tree_data['Flights'].fillna(0)

    # Convert the flights to integers
    tree_data['Flights'] = tree_data['Flights'].astype(int)

    # Return the results
    return tree_data

def get_sunburst_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the sunburst data for the given dataframe.

    Arguments:
    dataframe: Filtered dataframe.

    Returns:
    Dataframe containing the sunburst data.
    """
    # Prepare the cancelled data
    cancelled = dataframe[dataframe['Cancelled'] == 1].groupby(
        ["Reporting_Airline", "CancellationCode"]
    )["Flights"].sum().reset_index()

    #
    cancelled["Status"] = "Cancelled"

    #
    cancelled = cancelled.rename(columns={"CancellationCode": "Detail"})

    # Prepare the delay data
    arr_delayed = dataframe[dataframe['ArrDelay'] > 0].groupby(["Reporting_Airline", "Origin"])[
        "Flights"].sum().reset_index()
    arr_delayed["Detail"] = "Arrival Delay"

    #
    dep_delayed = dataframe[dataframe['DepDelay'] > 0].groupby(["Reporting_Airline", "Origin"])[
        "Flights"].sum().reset_index()
    dep_delayed["Detail"] = "Departure Delay"

    #
    delayed = pd.concat([arr_delayed, dep_delayed], ignore_index=True)
    delayed["Status"] = "Delayed"

    # Prepare the on-time data
    arr_ontime = dataframe[dataframe['ArrDelay'] == 0].groupby(["Reporting_Airline", "Origin"])[
        "Flights"].sum().reset_index()
    arr_ontime["Detail"] = "Arrival On-Time"

    #
    dep_ontime = dataframe[dataframe['DepDelay'] == 0].groupby(["Reporting_Airline", "Origin"])[
        "Flights"].sum().reset_index()
    dep_ontime["Detail"] = "Departure On-Time"

    #
    on_time = pd.concat([arr_ontime, dep_ontime], ignore_index=True)
    on_time["Status"] = "On-Time"

    # Combine all data
    sunburst_data = pd.concat([cancelled, delayed, on_time], ignore_index=True).sort_values(by="Reporting_Airline",
                                                                                            ascending=True)

    # Return the results
    return sunburst_data

def get_line_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the line data for the given dataframe.

    Arguments:
    dataframe: Filtered dataframe.

    Returns:
    Dataframe containing the line data.
    """
    # Group data by month and reporting airline
    line_data = dataframe.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()

    # Return the results
    return line_data

def compute_average_data(dataframe: pd.DataFrame):
    """
    Compute graph data for creating the yearly airline DELAY report.
    This function takes in airline data and selected year as an input
    and performs computation for creating charts and plots.

    Arguments:

    dataframe: Filtered dataframe.

    Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay
    """
    # Compute delay averages
    avg_car = dataframe.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()

    avg_weather = dataframe.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()

    avg_nas = dataframe.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()

    avg_sec = dataframe.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()

    avg_late = dataframe.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_car, avg_weather, avg_nas, avg_sec, avg_late

def create_choropleth(map_data: pd.DataFrame, airport_data: pd.DataFrame, selected_state=None, zoom_level=4):
    """
    Create a choropleth map of US states by flights with airport markers.

    :param map_data: the data for the map
    :param airport_data: the data for the airports
    :param selected_state: the selected state
    :param zoom_level: the zoom level

    :return:
    Plotly figure object
    """
    # Create the main choropleth map
    fig = px.choropleth(
        map_data,
        locations='StateCode',
        color='Flights',
        hover_data=['StateName', 'Flights'],
        locationmode='USA-states',
        color_continuous_scale='YlOrRd',
        range_color=[0, map_data['Flights'].max()],
        title="Choropleth Map of US States by Flights",
        labels={
            'StateCode': 'State Code',
            'Flights': 'Number of Flights',
            'StateName': 'State Name'
        }
    )

    # Add airport markers only if a state is selected
    if selected_state:

        # Get the state data
        state_data = states_coords_df[states_coords_df['Abbreviation'] == selected_state]
        state_name = state_data.iloc[0]['State']

        # Update the map layout with the selected state
        if not state_data.empty:
            # Get the coordinates
            coords = {"lat": state_data.iloc[0]['Latitude'], "lon": state_data.iloc[0]['Longitude']}

            # Update the layout with the selected state
            fig.update_layout(
                geo=dict(
                    center={"lat": coords["lat"], "lon": coords["lon"]},
                    projection_scale=zoom_level  # Zoom level
                )
            )

        # Filter airports in the selected state
        airports_in_state = airport_data[airport_data['StateCode'] == selected_state]

        # Add airport markers for each airport using a locator symbol
        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lat=airports_in_state['Latitude'],
                lon=airports_in_state['Longitude'],
                text=airports_in_state.apply(
                    lambda row: f"{row['AirportCode']}<br>Flights: {row['Flights']}", axis=1),
                marker=dict(
                    size=30,
                    color='black',
                    opacity=1,
                    symbol='x'
                ),
                name="Airport Locations"
            )
        )

        # Add scaled circles for flight volume
        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lat=airports_in_state['Latitude'],
                lon=airports_in_state['Longitude'],
                text=airports_in_state.apply(
                    lambda row: f"{row['AirportCode']}<br>Flights: {row['Flights']}", axis=1),
                marker=dict(
                    size=airports_in_state['Flights'] / airports_in_state['Flights'].max() * 100,  # Scale size
                    color='red',
                    opacity=0.5,
                    symbol='circle'
                ),
                name="Flight Volume"
            )
        )

        # Update the title
        fig.update_layout(title_text=f"Choropleth Map of {state_name}, US by Flights")

    # Return the figure
    return fig

def create_line(data: pd.DataFrame, state=None, airport=None):
    """
    Create a line chart based on the data provided, a state and an airport are optional.
    :param data: The data needed to create the chart
    :param state: A US state code, else set to None
    :param airport: A US-based airport code, else set to None
    :return: A line chart
    """

    # Create a general use of the line data
    air_time = data.groupby(["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values('AirTime',
                                                                                              ascending=False)

    # Determine the top 12 airlines
    top_airlines = air_time["Reporting_Airline"].tolist()[:12]

    # Create the plot data
    plot_data = data.groupby(["Reporting_Airline", "Month"])["AirTime"].sum().reset_index()

    # Create the line chart
    fig = px.line(
        plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
        x='Month',
        y='AirTime',
        color='Reporting_Airline',
        title='Average Monthly Flight Time per Airline in the US'
    )

    # When a state is provided
    if state:
        # Filter data by state
        state_data = data[data["StateCode"] == state]

        # Sort airlines of the state by their air time
        air_time = state_data.groupby(["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values('AirTime',
                                                                                                        ascending=False)

        # Determine the top airlines and save them in a list
        top_airlines = air_time["Reporting_Airline"].tolist()[:12]

        # Create the plot data
        plot_data = state_data.groupby(["Reporting_Airline", "StateCode", "Month"])["AirTime"].sum().reset_index()

        # Get the state's name safely
        state_name = state_data['StateName'].iloc[0] if not state_data.empty else state

        # Create the line chart accordingly
        fig = px.line(
            plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
            x='Month',
            y='AirTime',
            color='Reporting_Airline',
            title=f'Average Monthly Flight Time per Airline in {state_name}, US'
        )

    # When a state and an airport are provided
    if state and airport:
        # Filter data by state and airport
        airport_data = data[(data["StateCode"] == state) & (data["Origin"] == airport)]

        # Sort airlines operating in the airport by air time
        air_time = airport_data.groupby(
            ["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values('AirTime', ascending=False)

        # Determine the top airlines and save them in a list
        top_airlines = air_time["Reporting_Airline"].tolist()[:12]

        # Create the plot data
        plot_data = airport_data.groupby(["Reporting_Airline", "StateCode", "Month"])["AirTime"].sum().reset_index()

        # Get the state's name safely
        state_name = airport_data['StateName'].iloc[0] if not airport_data.empty else state

        # Create the line chart accordingly
        fig = px.line(
            plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
            x='Month',
            y='AirTime',
            color='Reporting_Airline',
            title=f'Average Monthly Flight Time per Airline at {airport} Airport in {state_name}, US'
        )

    # Return the result
    return fig
