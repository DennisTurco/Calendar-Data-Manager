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

            return data
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    def __extractTimeData(data):
        # Extract year from the Start column and convert Duration to timedelta
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])
        data['Year'] = data['Start'].dt.year

        # Calculate duration in hours
        data['Duration'] = pd.to_timedelta(data['End'] - data['Start']).dt.total_seconds() / 3600
        
        return data
    
    def __hoursBySummary(data):
        # Group by 'Summary' and calculate the sum of hours
        hours_by_summary = data.groupby('Summary')['Duration'].sum()
        
        #! TODO convert from hundredths to sixtieths (proportion -> x : val_hundredths = val_sixtieths : 100) 

        # Sort the DataFrame by total hours in descending order
        hours_by_summary = hours_by_summary.sort_values(ascending=False)
        
        return hours_by_summary
        
    @staticmethod
    def chart1(data):
        #################### Total Hours per Year
        # extract time
        data = Plotter.__extractTimeData(data)

        # Group by year and calculate the sum of hours
        yearly_hours = data.groupby('Year')['Duration'].sum()
        
        # Create a bar chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        ax = plt.bar(yearly_hours.index, yearly_hours)

        plt.xlabel('Year', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours per Year', fontsize=12)
        plt.xticks(yearly_hours.index)  # Ensure x-axis labels match available years
        
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)

        # Add text values above the bars
        for bar in ax:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05, f"{height:.2f}h", ha='center', va='center', color='black', fontsize=9)
        ####################
           
    @staticmethod
    def chart2(data):
        #################### Total Hours by Summary
        # extract time
        data = Plotter.__extractTimeData(data)

        hours_by_summary = Plotter.__hoursBySummary(data)

        # Create a bar chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        ax = hours_by_summary.plot(kind='bar', legend=False)

        plt.xlabel('Summary', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours by Summary', fontsize=12)
        
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)

        # Add text values above the bars
        for bar in ax.patches:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05, f"{height:.2f}h", ha='center', va='center', color='black', fontsize=9)
        ####################
        
    @staticmethod
    def chart3(data):
        #################### Total Hours by Summary Pie chart
        # extract time
        data = Plotter.__extractTimeData(data)

        hours_by_summary = Plotter.__hoursBySummary(data)

        # Create a pie chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        ax = hours_by_summary.plot(kind='pie', autopct='%1.1f%%', startangle=90)

        plt.xlabel('Summary', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours by Summary', fontsize=12)
        
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)

        plt.legend(title='Summary', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)  # Add legend outside the plot
        ####################
    
    #! TODO: fixhere  
    def chart4(data):
        #################### Total Hours by Summary and Year
        # extract time
        data = Plotter.__extractTimeData(data)
        
        # Group by 'Summary' and 'Year' and calculate the sum of hours
        summary_yearly_hours = data.groupby(['Year', 'Summary'])['Duration'].sum()

        # Unstack the DataFrame to have 'Summary' as columns
        summary_yearly_hours = summary_yearly_hours.unstack()

        # Plot the bar chart
        plt.figure(figsize=(12, 8))  # Adjust the figure size if needed
        ax = summary_yearly_hours.plot(kind='bar', stacked=True)
        
        plt.xlabel('Year', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours by Year and Summary', fontsize=12)
        plt.legend(title='Summary', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        ####################
   
    # TODO: ad a new frame that show all stats without any charts
    def allStats(data):
        # extract time
        data = Plotter.__extractTimeData(data) 
        
        # Group by year and calculate the sum of hours
        yearly_hours = data.groupby('Year')['Duration'].sum()
        
        hours_by_summary = Plotter.__hoursBySummary(data)
        
        summary_yearly_hours = data.groupby(['Year', 'Summary'])['Duration'].sum().unstack()
        
        print(f'''
        ---------------------
        Total Hours per Year
                {yearly_hours}
        ---------------------
        
        ---------------------
        Total Hours by Summary
                {hours_by_summary}
        ---------------------
        
        ---------------------
        Total Hours by Summary and Year
                {summary_yearly_hours}
        ---------------------
        ''')
    
           
    @classmethod
    def graph(cls, data):
        cls.chart1(data)
        cls.chart2(data)
        cls.chart3(data)
        #cls.chart4(data)
        
        cls.allStats(data)
        
        plt.tight_layout()
        plt.show()
        

#Plotter.graph(Plotter.loadData("C:/Users/Utente/Desktop/Dennis/Programmazione/GoogleCalendarDataManager/data/prova.csv"))