# Data Science in Health Care: Breast Cancer Detection


## Getting Started

### Overview
This project is basically an __Anomaly detection__ system, designed to provide a real-time score of data gathered to 
detect breast cancer in patients. The model beforehand is trained on the data to predict the likelihood of a patient. 
The data is collected from the __Wisconsin Breast Cancer Dataset__. The model is then deployed as-a-service to provide 
real-time predictions on new data.

### Aim
We know that early detection of breast cancer is crucial for the patient's survival. The aim of this project is to 
assist oncologists in detecting breast cancer in patients as early as possible. Besides delivering a high-accuracy, 
reliable, and efficient model, the project is a part of a case study designed to reinforce the trust in AI models and 
their applications in the health sector.

### About the Data
The data used in this project is the Wisconsin Breast Cancer Dataset. It is a dataset of breast cancer patients' 
measurements. The features are computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. 
They describe characteristics of the cell nuclei present in the image. The target variable is the diagnosis of the 
patient, which can be either malignant or benign. More on the data can be found 
[here](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)).

### Requirements
Use this prompt to install dependencies :
```shell 
pip install -r requirments.txt
```

### Data Stream

### Launch the model as a service (MaaS) 
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

If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of 
all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License — see the LICENSE file for details.


