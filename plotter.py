import datetime as dt
import io, subprocess, sys
import numpy as np


try:
    import pandas as pd
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd
try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties


class Plotter:    
    def __init__():
        pass
    
    def loadData(filepath):
        try: 
            # Load data from the CSV file
            data = pd.read_csv(filepath, sep='|', header=None, encoding='utf-8')
            return data
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
            
    def chart1(data):
        # Extracting titles and durations
        #parsed_data = [row.split('|') for row in data]
        df = pd.DataFrame(data, columns=['ID', 'Title', 'Start', 'End'])
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])

        # Calculating durations in hours
        df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600

        # Grouping durations by year for each title
        grouped = df.groupby(['Title', df['Start'].dt.year])['Duration'].sum().reset_index()

        # Plotting duration by year for each title
        plt.figure(figsize=(12, 8))
        for title in grouped['Title'].unique():
            data = grouped[grouped['Title'] == title]
            plt.plot(data['Start'], data['Duration'], label=title)

        plt.xlabel('Year')
        plt.ylabel('Total Duration (hours)')
        plt.title('Total Duration by Year for Each Title')
        plt.legend()
        plt.tight_layout()
    
    def chart2(data):
        # Extracting titles and durations
        #parsed_data = [row.split('|') for row in data]
        df = pd.DataFrame(data, columns=['ID', 'Title', 'Start', 'End'])
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])

        # Calculating durations in hours
        df['Duration'] = (df['End'] - df['Start']).dt.total_seconds() / 3600

        # Grouping durations by month for each title
        df['Month'] = df['Start'].dt.strftime('%Y-%m')  # Extracting month and year as a new column
        grouped = df.groupby(['Title', 'Month'])['Duration'].sum().reset_index()

        # Plotting duration by month for each title
        plt.figure(figsize=(12, 8))
        for title in grouped['Title'].unique():
            data = grouped[grouped['Title'] == title]
            plt.plot(data['Month'], data['Duration'], label=title)

        plt.xlabel('Month')
        plt.ylabel('Total Duration (hours)')
        plt.title('Total Duration by Month for Each Title')
        plt.legend()
        plt.tight_layout()
            
    def graph(data):
        Plotter.chart1(data)
        Plotter.chart2(data)
        
        plt.show() # Show the plot