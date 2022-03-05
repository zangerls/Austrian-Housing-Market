# Austrian Housing Market (ETL)

In this project I scraped the data of over 20.000 available properties in Austria, including postal code (and province), number of rooms, indoor area, garden area and price.
The data has subsequently been transformed and cleaned before being loaded into a local MariaDB database and temporarily being saved inside Python as Estate objects.

With every scraping of the web page, the data is also loaded into a csv file, which is used for training and testing three simple regression models to predict the house's price.
