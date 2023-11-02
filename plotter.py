import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from matplotlib.font_manager import FontProperties

# Load data from the CSV file
df = pd.read_csv('./data/data.csv', sep='|', header=None, encoding='ISO-8859-1')
df.columns = ['id', 'FirstName', 'LastName', 'Col3', 'Col4', 'Col5', 'DateTime', 'Col7', 'Duration', 'Col9']

#TODO: fixhere, i want to add utf8 for text
# Set the default font family to a font that supports Unicode characters
plt.rcParams['font.family'] = 'DejaVu Sans'


#################### Total Hours per Year
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

#################### Total Hours by Student
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
bars = hours_by_student.plot(kind='bar')
plt.xlabel('Student')
plt.ylabel('Total Hours')
plt.title('Total Hours by Student')
####################


# Show the plot
plt.tight_layout()
plt.show()
