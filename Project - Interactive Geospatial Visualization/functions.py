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
    # Prepare the canceled data
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

def create_choropleth(map_data: pd.DataFrame, airport_data: pd.DataFrame, selected_state=None, zoom_level=4):
    """
    Create a choropleth map of US states by flights with airport markers.

    :param map_data: The data for the map
    :param airport_data: The data for the airports
    :param selected_state: The selected state
    :param zoom_level: The zoom level

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

