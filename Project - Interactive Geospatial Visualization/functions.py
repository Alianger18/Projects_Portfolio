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
def get_state_name(state_code: str) -> str:
    """
    Get the state name from the state code.
    :param state_code: The state code.
    :return: The state name.
    """
    # Get the state name
    state_name = states_coords_df[states_coords_df['Abbreviation'] == state_code]['State'].values[0]

    # Return the result
    return state_name

def get_airports_data(dataframe: pd.DataFrame):
    """
    Get the airports data for the given dataframe.
    :param dataframe: Filtered dataframe.
    :return: Dataframe containing the airport's data.
    """
    # Aggregate airport-level data
    airport_flights = dataframe.groupby('Origin')['Flights'].sum().reset_index()

    # Rename the columns
    airport_flights.rename(columns={'Origin': 'AirportCode'}, inplace=True)

    # Merge the dataframes
    airport_data = pd.merge(airport_coords_df, airport_flights, on='AirportCode', how='left')

    # Fill missing values
    airport_data['Flights'] = airport_data['Flights'].fillna(0)

    # Convert the flights to integers
    airport_data['Flights'] = airport_data['Flights'].astype(int)

    # Sort the data
    airport_data.sort_values('StateName', ascending=True, inplace=True)

    # Return the results
    return airport_data

def get_map_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the map data for the given dataframe.
    :param dataframe: Filtered dataframe.
    :return: Dataframe containing the map data.
    """
    # Group data by state
    data = dataframe.groupby(['OriginState', 'OriginStateName'])['Flights'].sum().reset_index()

    # Fill missing values
    data['Flights'] = data['Flights'].fillna(0)

    # Convert the flights to integers
    data['Flights'] = data['Flights'].astype(int)

    # Rename the columns
    data.rename(columns={'OriginState': 'StateCode', 'OriginStateName' : 'StateName'}, inplace=True)

    # Sort the data
    data.sort_values('StateCode', ascending=True, inplace=True)

    # Return the results
    return data

def get_tree_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the tree data for the given dataframe.
    :param dataframe: Filtered dataframe.
    :return: Dataframe containing the tree data.
    """
    # Group data by state, airport, and airline
    data = dataframe.groupby(
        ['OriginState', 'Origin', 'Reporting_Airline']
    )['Flights'].sum().reset_index()
    data["Total Flights per state"] = data.groupby('OriginState')['Flights'].transform('sum')

    # Fill missing values
    data['Flights'] = data['Flights'].fillna(0)
    data["Total Flights per state"] = data["Total Flights per state"].fillna(0)
    data["Total Flights per airport"] = data.groupby('Origin')['Flights'].transform('sum')

    # Convert the flights to integers
    data['Flights'] = data['Flights'].astype(int)
    data["Total Flights per state"] = data["Total Flights per state"].astype(int)
    data["Total Flights per airport"] = data["Total Flights per airport"].astype(int)

    # Rename the columns
    data.rename(columns={'OriginState': 'StateCode'}, inplace=True)

    # Return the results
    return data

def get_sunburst_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the sunburst data for the given dataframe.
    :param dataframe: Filtered dataframe.
    :return: Dataframe containing the sunburst data.
    """

    # Prepare the cancelled data by filtering flights that were cancelled (Cancelled == 1)
    cancelled = dataframe[dataframe['Cancelled'] == 1].groupby(
        ["OriginState", "Origin", "Reporting_Airline", "CancellationCode"]
    )["Flights"].sum().reset_index()

    # Add a status column indicating these flights are 'Cancelled'
    cancelled["Status"] = "Cancelled"

    # Rename the 'CancellationCode' column to 'Detail' for consistency in final output
    cancelled = cancelled.rename(columns={"CancellationCode": "Detail"})

    # Prepare the delayed data by filtering flights that had an arrival delay (ArrDelay > 0)
    arr_delayed = dataframe[dataframe['ArrDelay'] > 0].groupby(["OriginState", "Origin", "Reporting_Airline"])[
        "Flights"].sum().reset_index()

    # Label these flights as "Arrival Delay" under 'Detail' column
    arr_delayed["Detail"] = "Arrival Delay"

    # Prepare the delayed data by filtering flights that had a departure delay (DepDelay > 0)
    dep_delayed = dataframe[dataframe['DepDelay'] > 0].groupby(["OriginState", "Origin", "Reporting_Airline"])[
        "Flights"].sum().reset_index()

    # Label these flights as "Departure Delay" under 'Detail' column
    dep_delayed["Detail"] = "Departure Delay"

    # Combine both arrival and departure delay data into a single dataframe
    delayed = pd.concat([arr_delayed, dep_delayed], ignore_index=True)

    # Add a status column indicating these flights are 'Delayed'
    delayed["Status"] = "Delayed"

    # Prepare the on-time data by filtering flights that had no arrival delay (ArrDelay == 0)
    arr_ontime = dataframe[dataframe['ArrDelay'] == 0].groupby(["OriginState", "Origin", "Reporting_Airline"])[
        "Flights"].sum().reset_index()

    # Label these flights as "Arrival On-Time" under 'Detail' column
    arr_ontime["Detail"] = "Arrival On-Time"

    # Prepare the on-time data by filtering flights that had no departure delay (DepDelay == 0)
    dep_ontime = dataframe[dataframe['DepDelay'] == 0].groupby(["OriginState", "Origin", "Reporting_Airline"])[
        "Flights"].sum().reset_index()

    # Label these flights as "Departure On-Time" under 'Detail' column
    dep_ontime["Detail"] = "Departure On-Time"

    # Combine both arrival and departure on-time data into a single dataframe
    on_time = pd.concat([arr_ontime, dep_ontime], ignore_index=True)

    # Add a status column indicating these flights are 'On-Time'
    on_time["Status"] = "On-Time"

    # Combine all three datasets (Cancelled, Delayed, and On-Time flights)
    data = pd.concat([cancelled, delayed, on_time], ignore_index=True).sort_values(
        by="Reporting_Airline", ascending=True
    )

    # Ensure the 'Flights' column contains integer values
    data["Flights"] = data["Flights"].astype(int)

    # Change column name
    data.rename(columns={'OriginState': 'StateCode'}, inplace=True)

    # Return the processed dataframe
    return data

def get_line_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Get the line data for the given dataframe.
    :param dataframe: Filtered dataframe.
    :return: Dataframe containing the line data.
    """
    # Group data by month and reporting airline
    data = dataframe.groupby(['OriginState', 'Origin', 'Month', 'Reporting_Airline'])['AirTime'].sum().reset_index()

    # Round the values
    data["AirTime"] = data["AirTime"].astype(int)

    # Rename the column
    data.rename(columns={'OriginState': 'StateCode'}, inplace=True)

    # Return the results
    return data

def create_choropleth(map_data: pd.DataFrame, airport_data: pd.DataFrame, selected_state=None, zoom_level=4):
    """
    Create a choropleth map of US states by flights with airport markers.
    :param map_data: the data for the map
    :param airport_data: the data for the airports
    :param selected_state: the selected state
    :param zoom_level: the zoom level
    :return: Plotly figure object
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
        title="Choropleth Map of Flights in the US",
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
        state_name = get_state_name(selected_state)

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
        fig.update_layout(title_text=f"Choropleth Map of Flights in {state_name}, US")

    # Return the figure
    return fig

def create_tree_map(data: pd.DataFrame, state=None, airport=None):
    """
    Create a treemap visualization for flight distribution.
    :param data: DataFrame containing flight data.
    :param state: Optional; State code to filter the data.
    :param airport: Optional; Airport code to filter the data.
    :return: Plotly treemap figure.
    """

    # Create the initial figure
    fig = px.treemap(
        data, color='Total Flights per state', values='Flights',
        path=['StateCode', 'Origin', 'Reporting_Airline'],
        color_continuous_scale='YlOrRd',
        title='Flights distribution across States and Airports in the US'
    )

    # Filter by state
    if state:

        # Create the figure
        fig = px.treemap(
            data[data['StateCode'] == state],
            color='Total Flights per airport', values='Flights',
            path=['StateCode', 'Origin', 'Reporting_Airline'], color_continuous_scale='YlOrRd',
            title=f'Flights distribution across airports in {get_state_name(state)}, US'
        )

    # Filter by state and airport
    if state and airport:

        # Create the figure
        fig = px.treemap(
            data[(data['Origin'] == airport) & (data['StateCode'] == state)],
            color='Flights', values='Flights',
            path=['StateCode', 'Origin', 'Reporting_Airline'], color_continuous_scale='YlOrRd',
            title=f'Flights distribution at the {airport} airport in {get_state_name(state)}, US'
        )

    # Return the results
    return fig

def create_sunburst(data: pd.DataFrame, state=None, airport=None, airline=None):
    """
    Create a sunburst visualization for airlines performances.
    :param data: DataFrame containing flight data.
    :param state: Optional; State code to filter the data.
    :param airport: Optional; Airport code to filter the data.
    :param airline: Optional; Airline name to filter the data.
    :return: Plotly Sunburst figure.
    """

    # Create the initial figure
    fig = px.sunburst(
        data, values="Flights", color="Status",
        path=["Reporting_Airline", "Status", "Detail"],
        color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
        title="Airlines performance in the US",
    )

    # Filter by state
    if state:

        # Create the figure
        fig = px.sunburst(
            data[data['StateCode'] == state], color="Status", values="Flights",
            path=["Reporting_Airline", "Status", "Detail"],
            color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
            title=f'Airlines performance in {get_state_name(state)}, US'
        )

    # Filter by state and airport
    if state and airport:

        # Create the figure
        fig = px.sunburst(
            data[(data['Origin'] == airport) & (data['StateCode'] == state)], color="Status", values="Flights",
            path=["Reporting_Airline", "Status", "Detail"],
            color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
            title=f'Airlines performance at the {airport} airport in {get_state_name(state)}, US',
        )

    # Filter by state, airport, and airline
    if state and airport and airline:

        # Prepare filtered data
        filtered_data = data[(data['StateCode'] == state) & (data['Origin'] == airport)]

        # Create the figure
        fig = px.sunburst(
            filtered_data[filtered_data['Reporting_Airline'] == airline], color="Status", values="Flights",
            path=["Reporting_Airline", "Status", "Detail"],
            color_discrete_map={"Cancelled": "red", "Delayed": "orange", "On-Time": "green"},
            title=f'{airline} Airlines performance at the {airport} airport in {get_state_name(state)}, US',
        )

    # Return the results
    return fig

def create_line(data: pd.DataFrame, state=None, airport=None, airline=None):
    """
    Create a line chart based on the data provided, a state and an airport are optional.
    :param data: The data needed to create the chart
    :param state: A US state code, else set to None
    :param airport: A US-based airport code, else set to None
    :param airline: An airline code, else set to None
    :return: A line chart
    """

    # Create a general use of the line data
    air_time = data.groupby(["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values(
        'AirTime', ascending=False
    )

    # Determine the top 10 airlines
    top_airlines = air_time["Reporting_Airline"].tolist()[:10]

    # Create the plot data
    plot_data = data.groupby(["Reporting_Airline", "Month"])["AirTime"].sum().reset_index()

    # Create the line chart
    fig = px.line(
        plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
        x='Month',
        y='AirTime',
        color='Reporting_Airline',
        title="Airlines' Monthly Flight Time in the US"
    )

    # When a state is provided
    if state:

        # Filter data by state
        state_data = data[data["StateCode"] == state]

        # Sort airlines of the state by their air time
        air_time = state_data.groupby(["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values(
            'AirTime', ascending=False)

        # Determine the top airlines and save them in a list
        top_airlines = air_time["Reporting_Airline"].tolist()[:10]

        # Create the plot data
        plot_data = state_data.groupby(["Reporting_Airline", "StateCode", "Month"])["AirTime"].sum().reset_index()

        # Get the state's name safely
        state_name = get_state_name(state)

        # Create the line chart accordingly
        fig = px.line(
            plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
            x='Month',
            y='AirTime',
            color='Reporting_Airline',
            title=f"Airlines' Monthly Flight Time in {state_name}, US"
        )

    # When a state and an airport are provided
    if state and airport:

        # Filter data by state and airport
        airport_data = data[(data["StateCode"] == state) & (data["Origin"] == airport)]

        # Sort airlines operating in the airport by air time
        air_time = airport_data.groupby(
            ["Reporting_Airline"])["AirTime"].sum().reset_index().sort_values('AirTime', ascending=False)

        # Determine the top airlines and save them in a list
        top_airlines = air_time["Reporting_Airline"].tolist()[:10]

        # Create the plot data
        plot_data = airport_data.groupby(["Reporting_Airline", "StateCode", "Month"])["AirTime"].sum().reset_index()

        # Get the state's name safely
        state_name = get_state_name(state)

        # Create the line chart accordingly
        fig = px.line(
            plot_data[plot_data["Reporting_Airline"].isin(top_airlines)],
            x='Month',
            y='AirTime',
            color='Reporting_Airline',
            title=f"Airlines' Monthly Flight Time at {airport} Airport in {state_name}, US"
        )

    # When a state, an airport, and an airline code are provided
    if state and airport and airline:

        # Filter data by state and airport
        airport_data = data[(data["StateCode"] == state) & (data["Origin"] == airport)]

        # Create the plot data
        plot_data = airport_data.groupby(["Reporting_Airline", "StateCode", "Month"])["AirTime"].sum().reset_index()

        # Get the state's name safely
        state_name = get_state_name(state)

        # Create the line chart accordingly
        fig = px.line(
            plot_data[plot_data["Reporting_Airline"] == airline],
            x='Month',
            y='AirTime',
            title=f"{airline} Airlines' Monthly Flight Time at {airport} Airport in {state_name}, US"
        )

    # Set the x-axis values
    fig.update_xaxes(
        tickmode='array',
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )

    # Return the result
    return fig
