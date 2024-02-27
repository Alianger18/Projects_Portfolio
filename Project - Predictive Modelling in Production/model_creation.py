# Importing the required libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import pandas as pd
from pathlib import Path

#
path = Path.cwd()

# Loading the data
data = pd.read_csv(f'{path}/data/data_v1.0.csv')

# Specifying the train/test data
x_train, x_test, y_train, y_test = train_test_split(
    data[['sound', 'temp', 'humidity']],
    data['score'],
    test_size=0.3
)

# Dictionary to store models and their respective performance metrics
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Support Vector Machine': SVR()
}

# Training and evaluating the models
results = {}
for name, model in models.items():
    model.fit(x_train, y_train)
    y_estimate = model.predict(x_test)
    mse = mean_squared_error(y_test, y_estimate)
    mae = mean_absolute_error(y_test, y_estimate)
    r2 = r2_score(y_test, y_estimate)
    results[name] = {'MSE': mse, 'MAE': mae, 'R-squared': r2}

# Print results
for name, metrics in results.items():
    print(f"Model: {name}")
    print(f"MSE: {metrics['MSE']}")
    print(f"MAE: {metrics['MAE']}")
    print(f"R-squared: {metrics['R-squared']}")
    print()

# Saving the best model (based on R-squared) in a pickle format
best_model_name = max(results, key=lambda x: results[x]['R-squared'])
best_model = models[best_model_name]
with open('best_model.pkl', 'wb') as file:
    pickle.dump(best_model, file)
