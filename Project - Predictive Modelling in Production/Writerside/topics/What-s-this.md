# What&apos;s this ?

This project is about building an anomaly detection system.

For this matter, our predictive model, a Linear Regression algorithm, uses 3 Key Performance Indicators (KPIs) Sound, 
Temperature, and Humidity measured in decibels (dB), Fahrenheit (°F), and percentage of Relative Humidity (RH) 
respectively.

The normal range of these KPIs are as follows :

* **Sound**       : 60 dB to 85 dB
* **Temperature** : 68°F  to 86°F
* **Humidity**    : 40%   to 60% of RH

This model attributes a score with 10 indicating the machinery is operating at its highest levels, degrading
this score means lower performances. The lowest accepted score which don't need an intervention is 3,0.

This score can be used to support decisions regarding whether a machinery necessitate technical attention or not.
