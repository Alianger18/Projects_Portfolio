# Predictive Modeling in Production


## Getting Started

### Overview
This project is an __Anomaly detection__ system, designed to provide a real-time score for measurements of data gathered 
from sensors of the manufacturing machines for one of VESTAS .inc sites based in __Travemünde, Denmark__. The system is 
designed to avoid latency in production lines and manufacturing faulty items through immediate intervention in the 
production site based on the score given by the model. 

The score is based on three parameters: Sound, Temperature, and Humidity. The normal ranges of the parameters are :
- **Sound** measured in deciBell (dB) — 60 dB to 85 dB.
- **Temperature** measured in Fahrenheit (°F) — 68°F  to 86°F
- **Humidity** measured in Relative Humidity — 40% to 60% of RH

The score is from 1 to 10 with 1 being the lowest and 10 the highest.
The more the parameters are at the lower end of their normal range, the higher is the score, and the more parameters are
at the higher end of their normal range, the lower is the score.


### Requirements
Use this prompt to install dependencies :
```shell 
pip install -r requirments.txt
```

### Data Stream
This project runs on a simulated measurements of the data. To run this stream, execute the following script :
```shell 
python data_stream.py
```

### Launch the model as a service (MAAS) 
After setting the data stream, launch the app :
```shell 
python main.py
```

### View the dashboard 
After setting the data stream and launching the app, the dashboard dash application is singularizing real time data :
```shell 
python dashboard.py
```

### Creating the model
Linear Regression is the model used for inference. Launch the notebook for more information on the model's choice, 
training, testing, and evaluation.
```shell 
jupyter notebook notebooks/Model_creation.ipynb
```

### Monitoring the model
For tracking purposes, consult the mlflow UI portal by executing the following command :
```shell 
mlflow ui -p 1234
```


## Contributing

If you would like to contribute to this project, please feel free to submit a 
pull request. We welcome contributions of all kinds, including bug fixes, 
feature requests, and code improvements.

## License

This project is licensed under the MIT License — see the LICENSE file for details.


