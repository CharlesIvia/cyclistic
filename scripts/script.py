# Import required packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime

sns.set_palette("Set2")
# Read data into dataframes

june_2020_df = pd.read_csv("./data/202006-divvy-tripdata.csv")
july_2020_df = pd.read_csv("./data/202007-divvy-tripdata.csv")
august_2020_df = pd.read_csv("./data/202008-divvy-tripdata.csv")
september_2020_df = pd.read_csv("./data/202009-divvy-tripdata.csv")
october_2020_df = pd.read_csv("./data/202010-divvy-tripdata.csv")
november_2020_df = pd.read_csv("./data/202011-divvy-tripdata.csv")
december_2020_df = pd.read_csv("./data/202012-divvy-tripdata.csv")
january_2021_df = pd.read_csv("./data/202101-divvy-tripdata.csv")
february_2021_df = pd.read_csv("./data/202102-divvy-tripdata.csv")
march_2021_df = pd.read_csv("./data/202103-divvy-tripdata.csv")
april_2021_df = pd.read_csv("./data/202104-divvy-tripdata.csv")
may_2021_df = pd.read_csv("./data/202105-divvy-tripdata.csv")

# Create a list of all dataframes

frames = [
    june_2020_df,
    july_2020_df,
    august_2020_df,
    september_2020_df,
    october_2020_df,
    november_2020_df,
    december_2020_df,
    january_2021_df,
    february_2021_df,
    march_2021_df,
    april_2021_df,
    may_2021_df,
]

# Check number of columns for all the dataframes
# This step is necessary as it informs whether and how the dataframes can be joined
num_cols = []


def verify_num_of_cols(frames):
    for frame in frames:
        num_cols.append(len(frame.columns))
    return num_cols


# print(verify_num_of_cols(frames=frames))
# Here, we establish that each dataframe has 13 columns
# By inspecting the columns manually, we discover that they are appropriately named
# across the dataframes

# Create a single dataframe that combines the 12 dataframes
df = pd.concat(frames, axis=0, ignore_index=True)
print(df.columns)

# Summary of the data
print(df.head(10))
print(df.info())

# DATA CLEANING

# First we need to establish which columns and rows have missing data
# Columns with missing values
print(df.isnull().sum())

# Rows missing values
print(df[df.isnull().any(axis=1)])

# Examine the first row with missing values further
print(df.iloc[800])

# Find out the total number of rows that contain null values
sum_of_rows_with_null_values = df.isnull().any(axis=1).sum()
print(f"Total Null rows: {sum_of_rows_with_null_values}")

# Percentage of rows with missing values in the dataset
pc_nan_rows = sum_of_rows_with_null_values / df.shape[0] * 100
print(f"PC of null rows: {pc_nan_rows}")

# Drop rows with missing data
# Since rows with missing data appear to contain more than one missing value and
# only account for 7.7% of the dataset, we drop them.
# We do not drop the columns because they have less than 5% missing values

clean_df = df.dropna(axis="index")

# Check if new df has any missing values
# This step confirms that the data has no missing values
print(clean_df.isnull().sum())

# Check if any ID's are duplicate
total_duplicate_rows = clean_df.duplicated().sum()
print(f"Duplicate rows: {total_duplicate_rows}")

# Cleaned dataframe
print(clean_df)
print(clean_df.info())

# PROCESS DATA

# transform started_at and ended_at into datetime

clean_df["started_at"] = pd.to_datetime(clean_df["started_at"])
clean_df["ended_at"] = pd.to_datetime(clean_df["ended_at"])

# Sort dataframe in descending order based on ended_at colum
clean_df.sort_values(by=["ended_at"], inplace=True, ascending=False)
print(clean_df)

# From above, we notice that the dataframe contains some data for June 2021.
# Below we remove june 2021 data so that months = 12

june_2021_filter = df["ended_at"] <= "2021-06-03 00:00:00"
clean_df = clean_df[june_2021_filter]

# Create ride_length column (ride_length is in minutes)
ride_length = clean_df["ended_at"] - clean_df["started_at"]
ride_length = np.round(ride_length.dt.total_seconds() / 60, 2)
clean_df["ride_length"] = ride_length

# day_of_week
# This colum will contain the day of the week a ride started
clean_df["day_of_week"] = clean_df["started_at"].dt.day_name()

# month columns
clean_df["month"] = pd.DatetimeIndex(clean_df["started_at"]).month
clean_df["month_name"] = clean_df["started_at"].dt.strftime("%b")
print(clean_df)

# Get a summary of the data
data_descrption = clean_df.describe()
print(data_descrption)

# From this summary:
# We note that there are some negative values  for ride length
# Below we take a better look at them

neg_ride_length = clean_df[clean_df["ride_length"] < 0]
print(f"Rows with negative ride length value {neg_ride_length}")

# 10k rows have negative values - we filter them out
clean_df = clean_df[clean_df["ride_length"] > 0]

# ANALYZE DATA

# SUMMARY
data_descrption = clean_df.describe()
print(data_descrption)

# From the new summary:
# The average ride_length is 26.98 minutes
# The minimum ride length is 1.2 seconds
# The maximum ride length is 904.72hours, approxiamately 38days

# TOTAL NUMBER OF RIDERS PER CATEGORY

total_riders = clean_df["member_casual"].value_counts()
print(f"Number of riders per category \n {total_riders}")

# Confirm the total number of bike-share riders
total_riders_using_id = clean_df.groupby(["member_casual"])["ride_id"].count()
print(f"Total riders using ride_id \n {total_riders_using_id}")

# Pie chart to show riders per category
fig, ax = plt.subplots(figsize=(7, 3), dpi=90)
labels = ["Member", "Casual"]
plt.pie(x=total_riders, autopct="%.1f%%", labels=labels)
ax.set_title("Total Bike Hires Per Rider Category", pad=14, loc="center")
plt.show()

# Find out how bike hires were distibuted throughout the year

ride_hires_per_month = (
    clean_df["month"]
    .value_counts(sort=False)
    .rename_axis("Month")
    .reset_index(name="Total Hires")
)

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
print(ride_hires_per_month)

plt.figure(figsize=(7, 3), dpi=90)
plt.title("Total Bike Hires per Month", loc="left", pad=14)
sns.barplot(data=ride_hires_per_month, x=months, y="Total Hires")
plt.show()


# Find out what days of the week have the most bike hires

ride_hires_per_day = (
    clean_df["day_of_week"]
    .value_counts()
    .rename_axis("Day")
    .reset_index(name="Total Hires")
)
ride_hires_per_day.sort_values(by=["Total Hires"], inplace=True, ascending=True)
print(ride_hires_per_day)

plt.figure(figsize=(7, 3), dpi=90)
plt.title("Total Bike Hires per Day of the Week", loc="left", pad=14)
sns.barplot(data=ride_hires_per_day, x="Day", y="Total Hires")
plt.show()

# BIKE HIRES PER CATEGORY PER MONTH
# Find out how ridership compares everymonth for the two rider categories

monthly_bike_hires_per_customer_category = clean_df.groupby(["member_casual"])[
    "month_name"
].value_counts(sort=True)

monthly_casual_member_df = pd.DataFrame()
monthly_casual_member_df["casual"] = monthly_bike_hires_per_customer_category["casual"]
monthly_casual_member_df["member"] = monthly_bike_hires_per_customer_category["member"]
monthly_casual_member_df["Month"] = monthly_casual_member_df.index


print(monthly_casual_member_df)

pos = list(range(len(monthly_casual_member_df["casual"])))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

plt.bar(pos, monthly_casual_member_df["casual"], width)
plt.bar([p + width for p in pos], monthly_casual_member_df["member"], width)

# Setting the y and x axis label
ax.set_ylabel("Total Hires")
ax.set_xlabel("Month")
# Setting the chart's title
ax.set_title("Total Bike Hires per Rider Category per Month", loc="left", pad=14)

# Setting the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

# Setting the labels for the x ticks
ax.set_xticklabels(monthly_casual_member_df["Month"])

# Adding the legend and showing the plot
plt.legend(["Casual", "Member"], loc="upper right")
plt.show()


# BIKE HIRES PER CATEGORY PER DAY
# Find out how ridership compares everyday for the two rider categories

bike_hires_per_customer_category = clean_df.groupby(["member_casual"])[
    "day_of_week"
].value_counts(sort=True)
print(bike_hires_per_customer_category)

casual_member_df = pd.DataFrame()
casual_member_df["casual"] = bike_hires_per_customer_category["casual"]
casual_member_df["member"] = bike_hires_per_customer_category["member"]
casual_member_df["Day"] = casual_member_df.index

print(casual_member_df)

pos = list(range(len(casual_member_df["casual"])))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

plt.bar(pos, casual_member_df["casual"], width)
plt.bar([p + width for p in pos], casual_member_df["member"], width)

# Setting the y and x axis label
ax.set_ylabel("Total Hires")
ax.set_xlabel("Day of the Week")
# Setting the chart's title
ax.set_title("Total Bike Hires per Rider Category per Day", loc="left", pad=14)

# Setting the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

# Setting the labels for the x ticks
ax.set_xticklabels(casual_member_df["Day"])

# Adding the legend and showing the plot
plt.legend(["Casual", "Member"], loc="upper right")
plt.show()


# AVERAGE RIDE LENGTH PER CATEGORY

average_ride_length = clean_df.groupby(["member_casual"])["ride_length"].mean()
print(f"The average ride length per category {average_ride_length}")

fig, ax = plt.subplots(figsize=(7, 3), dpi=90)
labels = ["Casual", "Member"]
plt.pie(x=average_ride_length, autopct="%.1f%%", labels=labels)
ax.set_title("Average Ride Length", pad=14, loc="center")
plt.show()

# AVERAGE RIDE LENGTH FOR RIDERS BY DAY OF THE WEEK

average_daily_ride_length = clean_df.groupby(["member_casual", "day_of_week"])[
    "ride_length"
].mean()
print(f"Average ride lenth per category per day {average_daily_ride_length}")

weekly_average_ride_length_df = pd.DataFrame()

weekly_average_ride_length_df["casual"] = average_daily_ride_length["casual"]
weekly_average_ride_length_df["member"] = average_daily_ride_length["member"]
weekly_average_ride_length_df["Day"] = weekly_average_ride_length_df.index

print(weekly_average_ride_length_df)

pos = list(range(len(weekly_average_ride_length_df["casual"])))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

plt.bar(pos, weekly_average_ride_length_df["casual"], width)
plt.bar([p + width for p in pos], weekly_average_ride_length_df["member"], width)

# Setting the y and x axis label
ax.set_ylabel("Average Ride Length")
ax.set_xlabel("Day of the Week")
# Setting the chart's title
ax.set_title("Average Ride Length per Rider Category per Day", loc="left", pad=14)

# Setting the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

# Setting the labels for the x ticks
ax.set_xticklabels(weekly_average_ride_length_df["Day"])

# Adding the legend and showing the plot
plt.legend(["Casual", "Member"], loc="upper right")
plt.show()


# AVERAGE RIDE LENGTH FOR RIDERS BY MONTH

average_daily_ride_length_per_month = clean_df.groupby(["member_casual", "month"])[
    "ride_length"
].mean()
print(f"Average ride lenth per category per day {average_daily_ride_length_per_month}")

monthly_average_ride_length_df = pd.DataFrame()

monthly_average_ride_length_df["casual"] = average_daily_ride_length_per_month["casual"]
monthly_average_ride_length_df["member"] = average_daily_ride_length_per_month["member"]
monthly_average_ride_length_df["month"] = monthly_average_ride_length_df.index

print(monthly_average_ride_length_df)

pos = list(range(len(monthly_average_ride_length_df["casual"])))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 3), dpi=90)

plt.bar(pos, monthly_average_ride_length_df["casual"], width)
plt.bar([p + width for p in pos], monthly_average_ride_length_df["member"], width)

# Setting the y and x axis label
ax.set_ylabel("Average Ride Length")
ax.set_xlabel("Month")
# Setting the chart's title
ax.set_title("Average Ride Length per Rider Category per Month", loc="left", pad=14)

# Setting the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

# Setting the labels for the x ticks
ax.set_xticklabels(months)

# Adding the legend and showing the plot
plt.legend(["Casual", "Member"], loc="upper right")
plt.show()

# RIDEABLE TYPE PER RIDER CATEGORY
type_of_bike = clean_df.groupby(["member_casual"])["rideable_type"].value_counts()
print(type_of_bike)
