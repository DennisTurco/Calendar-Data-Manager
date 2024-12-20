import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import webbrowser
import tempfile
import os

class Plotter:
    
    @staticmethod
    def loadData(filepath):
        # check if file exists and if it is empty
        if not os.path.isfile(filepath): raise FileNotFoundError()
        if os.stat(filepath).st_size == 0: raise pd.errors.EmptyDataError()
        
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
            
            # Remove character 'Z'
            data['Start'] = data['Start'].str.replace('Z', '')
            data['End'] = data['End'].str.replace('Z', '')
            
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
        except pd.errors.ParserError as parser_error:
            raise pd.errors.ParserError(f"Parsing error: {str(parser_error)}")
        except ValueError as value_error:
            raise ValueError(f"Value error: {str(value_error)}")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
    
    @staticmethod
    def __extractTimeData(data):
        # Extract year from the Start column and convert Duration to timedelta
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])
        data['Year'] = data['Start'].dt.year
        data['Month'] = data['Start'].dt.month

        # Calculate duration in hours
        data['Duration'] = pd.to_timedelta(data['End'] - data['Start']).dt.total_seconds() / 3600
        
        return data
    
    @staticmethod
    def __hoursBySummary(data):
        # Group by 'Summary' and calculate the sum of hours
        hours_by_summary = data.groupby('Summary')['Duration'].sum()
        
        #! TODO convert from hundredths to sixtieths (proportion -> x : val_hundredths = val_sixtieths : 100) 

        # Sort the DataFrame by total hours in descending order
        hours_by_summary = hours_by_summary.sort_values(ascending=False)
        
        return hours_by_summary
        
    @staticmethod
    def __chart1(data):
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
    def __chart2(data):
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
    def __chart3(data):
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
    @staticmethod
    def __chart4(data):
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
        
    @staticmethod
    def chart_TotalHoursPerYear(data):
        #################### Total Hours per Year
        # Extract time data
        data = Plotter.__extractTimeData(data)

        # Group by year and calculate the sum of hours
        yearly_hours = data.groupby('Year')['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(yearly_hours, x='Year', y='Duration', labels={'Year': 'Year', 'Duration': 'Total Hours'}, title='Total Hours per Year')

        # Add text values above the bars
        for i, row in yearly_hours.iterrows():
            fig.add_annotation(x=row['Year'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=yearly_hours['Year'], ticktext=yearly_hours['Year']))

        # Show the plot
        fig.show()
        ####################
    
    @staticmethod
    def chart_TotalHoursPerMonth(data):
        #################### Total Hours per Month
        # Extract time data
        data = Plotter.__extractTimeData(data)

        # Group by month and calculate the sum of hours
        monthly_hours = data.groupby('Month')['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(monthly_hours, x='Month', y='Duration', labels={'Month': 'Month', 'Duration': 'Total Hours'}, title='Total Hours per Month')

        # Add text values above the bars
        for i, row in monthly_hours.iterrows():
            fig.add_annotation(x=row['Month'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=monthly_hours['Month'], ticktext=monthly_hours['Month']))

        # Show the plot
        fig.show()
        ####################
        
    @staticmethod
    def chart_TotalHoursPerMonthGroupedByYear(data):
        #################### Total Hours per Month Grouped by Year
        # Extract time data
        data = Plotter.__extractTimeData(data)

        # Group by month, year, and calculate the sum of hours
        monthly_hours_by_year = data.groupby(['Month', 'Year'])['Duration'].sum().reset_index()

        # Create a bar chart with Plotly, color by 'Year'
        fig = px.bar(
            monthly_hours_by_year,
            x='Month',
            y='Duration',
            color='Year',
            labels={'Month': 'Month', 'Duration': 'Total Hours'},
            title='Total Hours per Month Grouped by Year',
            text_auto=True  # Automatically align values
        )

        # Ensure text annotations are centered inside each bar segment
        fig.for_each_trace(lambda trace: trace.update(
            textposition='inside',  # Position text inside the bar
            textfont=dict(size=12),  # Adjust font size for better readability
        ))

        # Customize layout
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=monthly_hours_by_year['Month'].unique(),
                ticktext=[f"Month {i}" for i in monthly_hours_by_year['Month'].unique()]
            ),
            yaxis=dict(
                title="Total Hours"
            ),
            coloraxis_colorbar=dict(
                tickvals=sorted(monthly_hours_by_year['Year'].unique()),  # Unique year ticks
                title="Year"
            ),
            title=dict(
                text='Total Hours per Month Grouped by Year',
                x=0.5  # Center the title
            )
        )

        # Show the plot
        fig.show()
        ####################
    
    @staticmethod
    def chart_TotalHoursBySummary(data):
        #################### Total Hours by Summary
        # Extract time
        data = Plotter.__extractTimeData(data)
        
        hours_by_summary = Plotter.__hoursBySummary(data)

        # Convert Series to DataFrame
        hours_by_summary_df = pd.DataFrame({'Summary': hours_by_summary.index, 'Duration': hours_by_summary.values})

        # Create a bar chart using Plotly Express
        fig = px.bar(hours_by_summary_df, x='Summary', y='Duration', labels={'Duration': 'Total Hours'}, title='Total Hours by Summary')

        # Add text values above the bars
        for i, val in enumerate(hours_by_summary):
            fig.add_annotation(x=i, y=val + 0.05, text=f"{val:.2f}h", showarrow=False)

        # Show the plot
        fig.show()
        ####################
            
    @staticmethod
    def chart_TotalHoursBySummaryPie(data):
        #################### Total Hours by Summary Pie chart
        # Extract time
        data = Plotter.__extractTimeData(data)

        hours_by_summary = Plotter.__hoursBySummary(data)

        # Create a pie chart using Plotly Express
        fig = px.pie(hours_by_summary, values='Duration', names=hours_by_summary.index, labels={'Duration': 'Total Hours', 'names': 'Summary'}, title='Total Hours by Summary Pie chart')

        # Show the plot
        fig.show()
        ####################
    
    @staticmethod
    def chart_TotalHoursPerYearBySummary(data):
        #################### Total Hours per Year by Summary
        # Extract time data
        data = Plotter.__extractTimeData(data)

        # Group by year and summary, calculate the sum of hours
        yearly_hours_by_summary = data.groupby(['Year', 'Summary'])['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(yearly_hours_by_summary, x='Year', y='Duration', color='Summary',
                    labels={'Year': 'Year', 'Duration': 'Total Hours'}, title='Total Hours per Year by Summary')

        # Add text values above the bars
        for i, row in yearly_hours_by_summary.iterrows():
            fig.add_annotation(x=row['Year'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=yearly_hours_by_summary['Year'],
                                    ticktext=yearly_hours_by_summary['Year']))

        # Show the plot
        fig.show()
        ####################
    
    @staticmethod
    def chart_TotalHoursPerMonthBySummary(data):
        #################### Total Hours per Month by Summary
        # Extract time data
        data = Plotter.__extractTimeData(data)

        # Group by month and summary, calculate the sum of hours
        monthly_hours_by_summary = data.groupby(['Month', 'Summary'])['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(monthly_hours_by_summary, x='Month', y='Duration', color='Summary',
                    labels={'Month': 'Month', 'Duration': 'Total Hours'}, title='Total Hours per Month by Summary')

        # Add text values above the bars
        for i, row in monthly_hours_by_summary.iterrows():
            fig.add_annotation(x=row['Month'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=monthly_hours_by_summary['Month'],
                                    ticktext=monthly_hours_by_summary['Month']))

        # Show the plot
        fig.show()
        ####################
    
    @staticmethod
    def allStats(data):
        # extract time
        data = Plotter.__extractTimeData(data) 
        
        # Group by year and calculate the sum of hours
        yearly_hours = data.groupby('Year')['Duration'].sum()
        
        hours_by_summary = Plotter.__hoursBySummary(data)
        
        summary_yearly_hours = data.groupby(['Year', 'Summary'])['Duration'].sum().unstack()
        
        stats = [yearly_hours, hours_by_summary]
        
        # Save the full error details to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt") as temp_file:
            for stat in stats:  
                temp_file.write(str(stat) + '\n\n')
        
        webbrowser.open(f'file://{temp_file.name}')