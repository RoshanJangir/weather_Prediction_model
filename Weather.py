# ---------- 1. Load and preprocess data ----------
# Load the dataset
from datetime import datetime

import pandas as p
import pandas as pd

data = pd.read_csv(r"D:\weatherHistory.csv")

# Parse 'Formatted Date' column with UTC to handle mixed time zones
data['Formatted Date'] = pd.to_datetime(data['Formatted Date'], errors='coerce', utc=True)

# Rename columns and keep only what's needed
data = data.rename(columns={'Formatted Date': 'time', 'Temperature (C)': 'tavg'})
data = data[['time', 'tavg']].dropna()

# Ensure datetime format is correct
if not pd.api.types.is_datetime64_any_dtype(data['time']):
    raise TypeError("❌ The 'time' column is not in datetime format. Please check your CSV file.")

# Filter data to only include years from 2006 to 2017 (inclusive)
data = data[(data['time'].dt.year >= 2006) & (data['time'].dt.year <= 2017)]
data['day_of_year'] = data['time'].dt.dayofyear

# Calculate the average temperature for each day of the year across all years 2006-2017
daily_avg = data.groupby('day_of_year')['tavg'].mean().reset_index()


# ---------- 2. Temperature prediction function ----------
def predict_temperature_for_date(future_date_str):
    try:
        # Parse user input date
        future_date = datetime.strptime(future_date_str, '%Y-%m-%d')
        day_of_year = future_date.timetuple().tm_yday

        # Look up temperature from the 2006-2017 daily average
        temp_row = daily_avg[daily_avg['day_of_year'] == day_of_year]
        if temp_row.empty:
            print(f"⚠️ No data available for day {day_of_year} in the 2006-2017 dataset.")
            return

        temp = temp_row['tavg'].values[0]
        print(f"\n🌤 Forecast for {future_date.date()} (based on 2006-2017 average): {temp:.2f} °C")

    except ValueError:
        print("❌ Please enter the date in YYYY-MM-DD format.")


# ---------- 3. Runtime user input ----------
user_input = input("📅 Enter a future date (YYYY-MM-DD): ")
predict_temperature_for_date(user_input)

