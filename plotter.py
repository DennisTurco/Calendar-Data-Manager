import pandas as pd
import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def loadData(filepath):
        try: 
            # Load data from the CSV file
            data = pd.read_csv(filepath, sep='|', header=None, encoding='utf-8')
            data.columns = ['ID', 'Summary', 'Start', 'End', 'Duration']

            # Extract date without the additional time information
            data['Start'] = data['Start'].str.split('+').str[0]
            data['End'] = data['End'].str.split('+').str[0]
            
            # Remove character 'T'
            data['Start'] = data['Start'].str.replace('T', ' ')
            data['End'] = data['End'].str.replace('T', ' ')
            
            # Set the hours, minutes, and seconds if they are missing
            for index, elem in enumerate(data['Start']):
                if len(elem) == 10:
                    data.loc[index, 'Start'] = elem + " 00:00:00"
            for index, elem in enumerate(data['End']):
                if len(elem) == 10:
                    data.loc[index, 'End'] = elem + " 00:00:00"

            # Convert the 'Start' and 'End' columns to datetime with the correct format
            data['Start'] = pd.to_datetime(data['Start'], format='%Y-%m-%d %H:%M:%S')
            data['End'] = pd.to_datetime(data['End'], format='%Y-%m-%d %H:%M:%S')

            # Calculate the duration in hours
            data['Duration'] = pd.to_timedelta(data['Duration']).dt.total_seconds() / 3600

            return data
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    @staticmethod
    def chart1(data):
        #################### Total Hours per Year
        # Extract year from the Start column and convert Duration to timedelta
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])
        data['Year'] = data['Start'].dt.year

        # Calculate duration in hours
        data['Duration'] = (data['End'] - data['Start']).dt.total_seconds() / 3600

        # Group by year and calculate the sum of hours
        yearly_hours = data.groupby('Year')['Duration'].sum()
        
        # Create a bar chart
        plt.bar(yearly_hours.index, yearly_hours)
        plt.xlabel('Year')
        plt.ylabel('Total Hours')
        plt.title('Total Hours per Year')
        plt.xticks(yearly_hours.index)  # Ensure x-axis labels match available years
        ####################
           
    @staticmethod
    def chart2(data):
        #################### Total Hours by Summary
        # Convert 'Start' and 'Duration' columns
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])
        
        # Calculate duration in hours
        data['Duration'] = (data['End'] - data['Start']).dt.total_seconds() / 3600

        # Group by 'Summary' and calculate the sum of hours
        hours_by_summary = data.groupby('Summary')['Duration'].sum()

        # Sort the DataFrame by total hours in descending order
        hours_by_summary = hours_by_summary.sort_values(ascending=False)

        # Create a bar chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        hours_by_summary.plot(kind='bar')
        plt.xlabel('Summary')
        plt.ylabel('Total Hours')
        plt.title('Total Hours by Summary')
        ####################
        
    @staticmethod
    def chart3(data):
        #################### Total Hours by Summary Pie chart
        # Convert 'Start' and 'Duration' columns
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])

        # Calculate duration in hours
        data['Duration'] = (data['End'] - data['Start']).dt.total_seconds() / 3600

        # Group by 'Summary' and calculate the sum of hours
        hours_by_summary = data.groupby('Summary')['Duration'].sum()   

        # Sort the DataFrame by total hours in descending order
        hours_by_summary = hours_by_summary.sort_values(ascending=False)

        # Create a bar chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        hours_by_summary.plot(kind='pie')
        plt.xlabel('Summary')
        plt.ylabel('Total Hours')
        plt.title('Total Hours by Summary')
        ####################

            
    @classmethod
    def graph(cls, data):
        cls.chart1(data)
        cls.chart2(data)
        cls.chart3(data)
        
        plt.tight_layout()
        plt.show()