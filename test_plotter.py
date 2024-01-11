import datetime as dt
import io, subprocess, sys

try:
    import pandas as pd
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
    import pandas as pd
try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties


def loadData():
    # Load data from the CSV file
    df = pd.read_csv('./data/data.csv', sep='|', header=None, encoding='utf-8')
    df.columns = ['id', 'FirstName', 'LastName', 'Col3', 'Col4', 'Col5', 'DateTime', 'Col7', 'Duration', 'Col9']
    return df

#TODO: fixhere, i want to add utf8 for text
# Set the default font family to a font that supports Unicode characters
plt.rcParams['font.family'] = 'DejaVu Sans'


#################### Total Hours per Year
df = loadData()
# Extract year from the DateTime column and convert Duration to timedelta
df['DateTime'] = pd.to_datetime(df['DateTime'], utc=True)
df['Year'] = df['DateTime'].dt.year
df['Duration'] = pd.to_timedelta(df['Duration']).dt.total_seconds() / 3600  # Convert to hours

# Group by year and calculate the sum of hours
yearly_hours = df.groupby('Year')['Duration'].sum()

# Create a bar chart
plt.bar(yearly_hours.index, yearly_hours)
plt.xlabel('Year')
plt.ylabel('Total Hours')
plt.title('Total Hours per Year')
plt.xticks(yearly_hours.index)  # Ensure x-axis labels match available years
####################

#################### Total Hours per Month 2021 - 2022 - 2023
df = loadData()

# Convert 'DateTime' and 'Duration' columns
df['DateTime'] = pd.to_datetime(df['DateTime'], utc=True)
df['Duration'] = pd.to_timedelta(df['Duration']).dt.total_seconds() / 3600  # Convert to hours

# Create a new column 'Year' to extract the year from 'DateTime'
df['Year'] = df['DateTime'].dt.year

# Filter the data for the years 2021, 2022, and 2023
df_2021 = df[df['Year'] == 2021]
df_2022 = df[df['Year'] == 2022]
df_2023 = df[df['Year'] == 2023]

# Group by month and calculate the sum of hours for each year
hours_by_month_2021 = df_2021.groupby(df_2021['DateTime'].dt.month)['Duration'].sum()
hours_by_month_2022 = df_2022.groupby(df_2022['DateTime'].dt.month)['Duration'].sum()
hours_by_month_2023 = df_2023.groupby(df_2023['DateTime'].dt.month)['Duration'].sum()

# Create a single window with three subplots for 2021, 2022, and 2023
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Total Hours per Month', fontsize=16)

# Plot the bar charts for each year
def plot_bar_chart(data, year, ax):
    bars = data.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel('Month', fontproperties=FontProperties(family='DejaVu Sans', style='normal', size=12))
    ax.set_ylabel('Total Hours', fontproperties=FontProperties(family='DejaVu Sans', style='normal', size=12))
    ax.set_title(f'{year}', fontproperties=FontProperties(family='DejaVu Sans', style='normal', size=14))

    for i, v in enumerate(data):
        ax.text(i, v + 1, str(round(v, 2)), ha='center', va='bottom', fontproperties=FontProperties(family='DejaVu Sans', style='normal', size=10))

plot_bar_chart(hours_by_month_2021, 2021, axes[0])
plot_bar_chart(hours_by_month_2022, 2022, axes[1])
plot_bar_chart(hours_by_month_2023, 2023, axes[2])
####################

#################### Total Hours by Student
df = loadData()
# Convert 'DateTime' and 'Duration' columns
df['DateTime'] = pd.to_datetime(df['DateTime'], utc=True)
df['Duration'] = pd.to_timedelta(df['Duration']).dt.total_seconds() / 3600  # Convert to hours

# Create a new column 'Student' combining 'FirstName' and 'LastName' or 'FirstName' alone
df['Student'] = df.apply(lambda row: row['FirstName'] if pd.isnull(row['LastName']) else f"{row['FirstName']} {row['LastName']}", axis=1)

# Group by 'Student' and calculate the sum of hours
hours_by_student = df.groupby('Student')['Duration'].sum()

# Sort the DataFrame by total hours in descending order
hours_by_student = hours_by_student.sort_values(ascending=False)

# Create a bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
hours_by_student.plot(kind='bar')
plt.xlabel('Student')
plt.ylabel('Total Hours')
plt.title('Total Hours by Student')
####################


# Show the plot
plt.tight_layout()
plt.show()