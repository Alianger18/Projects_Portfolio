# Interactive Geospatial Visualization
Geospatial static visualization on its own helps present tons of information to the audience in a way that is 
straightforward to understand and interpret. 
However, turning them into interactive charts makes the visualization more intuitive and engaging for the users. 
In this project, we tend to create an interactive geospatial visualization tool that allows users to explore US Domestic
flights over the passed two-decade data in a more intuitive way. 


## About the project
In this project, we aim to create an interactive geospatial visualization tool that allows users to explore US Domestic 
flights over the passed two-decade data in a more intuitive way. 
The tool is designed to be interactive and explanatory, 
i.e., the user will be helped while using the tool to filter the number of flights per state, 
per airport in that state, per airline in the selected airport and state. 
The Airlines' performances are put into the sword by being examined to see the number of on-time, delayed, and canceled 
flights. 
Eventually, the air time of the flights is also examined to see the overall performance of the airlines.

The tool will be built using Python, Plotly, and Dash.

## About the data
The [data](https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/airline_2m.tar.gz) 
used in this notebook is only a sample from the original dataset called __The Reporting Carrier On-Time Performance 
Dataset__ containing information on approximately 200 million domestic US flights 
reported to the [United States Bureau of Transportation Statistics](https://www.bts.gov/). 
The dataset contains basic information about each flight (such as date, time, departure airport, arrival airport) and, 
if applicable, the amount of time the flight was delayed and information about the reason for the delay. 
A complete overview on the glossary of the data could be found [here](https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/data-preview/index.html).

__NOTE__: Due to its large size, it's recommended to download it manually.


## Installation

Start by installing project's requirements
```shell 
pip install -r requirements.txt
```

Then, launch the jupyter notebook 
```Shell 
jupyter notebook notebooks/notebook.ipynb
```

Finally, launch the dashboard locally
```shell
python main.py
```

## Snapshots

<img src="./notebooks/Final Dashboard.gif" alt="The Final Dashboard" width="2000">


## Contributing

If you would like to contribute to this project, please feel free to submit a pull request.
We welcome contributions of all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License—see the LICENSE file for details.
