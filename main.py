import mysql.connector
import pandas as pd
from fbprophet import Prophet

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create a cursor object
cursor = connection.cursor()

# Fetch website visit data from the database
cursor.execute("SELECT visit_date, visit_count FROM website_visits")
rows = cursor.fetchall()

# Convert the fetched data into a pandas DataFrame
df = pd.DataFrame(rows, columns=["visit_date", "visit_count"])

# Prepare the DataFrame for Prophet
df = df.rename(columns={"visit_date": "ds", "visit_count": "y"})

# Fit the Prophet model to the data
model = Prophet()
model.fit(df)

# Make predictions for the next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Calculate the upper and lower bounds for anomalies
forecast["yhat_lower"] = forecast["yhat"] - 3 * forecast["yhat_std"]
forecast["yhat_upper"] = forecast["yhat"] + 3 * forecast["yhat_std"]

# Merge the original data and the forecast data
anomaly_df = pd.merge(df, forecast[["ds", "yhat_lower", "yhat_upper"]], left_on="ds", right_on="ds")

# Find anomalies
anomalies = anomaly_df[(anomaly_df["y"] < anomaly_df["yhat_lower"]) | (anomaly_df["y"] > anomaly_df["yhat_upper"])]

# Insert the anomalies back into the database
for row in anomalies.itertuples(index=False):
    cursor.execute(
        "INSERT INTO website_visit_anomalies (visit_date, visit_count, yhat_lower, yhat_upper) VALUES (%s, %s, %s, %s)",
        (row.ds, row.y, row.yhat_lower, row.yhat_upper)
    )

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()
