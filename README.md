# Time Series Anomaly Detection using Prophet

This script detects anomalies in the time series data of website visits using the Prophet library by Facebook. It fetches website visit data from a MySQL database, fits a Prophet model to the data, makes predictions, calculates the upper and lower bounds for anomalies, and inserts the detected anomalies back into the database.

## Requirements

To run this script, you will need the following Python packages:

-   mysql-connector-python
-   pandas
-   fbprophet

You can install these packages using pip:

bashCopy code

`pip install mysql-connector-python pandas fbprophet` 

## Database Configuration

Before running the script, you need to configure the MySQL database connection parameters. Replace the following placeholder values with your database credentials:

-   `your_username`
-   `your_password`
-   `your_database`

pythonCopy code

`connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)` 

## Database Tables

This script assumes that the following tables exist in your database:

1.  `website_visits`: Stores the website visit data with columns `visit_date` and `visit_count`.
2.  `website_visit_anomalies`: Stores the detected anomalies with columns `visit_date`, `visit_count`, `yhat_lower`, and `yhat_upper`.

Make sure to create these tables with the appropriate schema before running the script.

## Running the Script

Once you have set up the database and installed the required packages, simply run the script using Python:

bashCopy code

`python time_series_anomaly_detection.py` 

The script will fetch the website visit data, fit a Prophet model, make predictions, and insert the detected anomalies into the `website_visit_anomalies` table in your database.
