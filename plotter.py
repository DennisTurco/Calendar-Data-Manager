import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

# Load data from the CSV file
df = pd.read_csv('./data/data.csv', sep='|', header=None, encoding='ISO-8859-1')
df.columns = ['id', 'FirstName', 'LastName', 'Col3', 'Col4', 'Col5', 'DateTime', 'Col7', 'Duration', 'Col9']


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

# Show the plot
plt.show()