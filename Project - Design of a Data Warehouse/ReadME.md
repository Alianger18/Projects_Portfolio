# What is it?
The project is suggesting the construction of a Data Warehouse (DWH) and using the Business Intelligence (BI) tools to 
provide valuable insights from the stored data. This proposal involves identifying source systems, such as operational 
and departmental systems, to provide data for the DWH. A suitable DWH architecture will be proposed by evaluating 
different variants and discussing their pros and cons. Additionally, one key performance indicator (KPI) will be 
selected to provide a concrete example. The goal is to enhance transparency, implement KPIs, and reduce manual data 
consolidation across departments.

In this repository, the __Project Report__ offers a thorough exploration on this project while the __Jupyter Notebook__ 
 showcases the process of building one of the Data Marts and how the data is processed to be ready for exploration using 
BI solutions.

# Why ?
The need to manage and analyze vast amounts of data effectively is forever growing. Modern organizations face several 
challenges in handling disparate data systems, which often leads to inefficiencies, data silos, and a lack of 
transparency in decision-making processes. 

Organizations seek to centralize data from various source systems—operational, departmental, and external—into a single,
coherent structure that enhances data accessibility and accuracy. This unified platform enables data consolidation, 
which reduces the manual effort required to compile reports across departments and improves data governance.

Furthermore, implementing BI tools on top of this DWH architecture allows organizations to extract actionable insights, 
track KPIs, and make data-driven decisions that align with business goals. This not only improves operational efficiency
but also provides real-time performance metrics, leading to better forecasting, resource management, and strategic 
planning.

## Installation

```shell 
pip install -r requirements.txt
```

## Usage

To install the database on PostgreSQL 
```shell
psql -U username -d database_name -f main_db.sql
```

To launch the notebook
```Shell 
jupyter notebook notebook.ipynb

```

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of 
all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
