from typing import Any, Dict, List, Union
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import webbrowser
import tempfile
import os

class Plotter:

    @staticmethod
    def _normalize_datetime_columns(data: pd.DataFrame) -> pd.DataFrame:
        """Normalize and convert Start/End columns to datetime."""
        for col in ['Start', 'End']:
            data[col] = (
                data[col]
                .astype(str)
                .str.split('+').str[0]
                .str.replace('T', ' ', regex=False)
                .str.replace('Z', '', regex=False)
            )

            # Add missing time part (YYYY-MM-DD)
            data[col] = data[col].where(
                data[col].str.len() > 10,
                data[col] + " 00:00:00"
            )

            data[col] = pd.to_datetime(
                data[col],
                format='%Y-%m-%d %H:%M:%S',
                errors='raise'
            )

        return data

    @staticmethod
    def load_data_from_csv(filepath: str) -> pd.DataFrame:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        if os.stat(filepath).st_size == 0:
            raise pd.errors.EmptyDataError("CSV file is empty")

        try:
            data = pd.read_csv(filepath, sep='|', header=None, encoding='utf-8')
            data.columns = ['ID', 'Summary', 'Start', 'End', 'Duration']
            return Plotter._normalize_datetime_columns(data)

        except Exception as e:
            raise RuntimeError(f"Failed to load CSV data: {e}") from e

    @staticmethod
    def load_data_from_list(events: List[Any]) -> pd.DataFrame:
        if not events:
            return pd.DataFrame(columns=['ID', 'Summary', 'Start', 'End', 'Duration'])

        rows = []

        for event in events:
            start = event.get('start', {})
            end = event.get('end', {})

            start_value = start.get('dateTime') or start.get('date')
            end_value = end.get('dateTime') or end.get('date')

            if not start_value or not end_value:
                continue

            rows.append({
                'ID': event.get('id'),
                'Summary': event.get('summary', ''),
                'Start': start_value,
                'End': end_value,
                'Duration': None
            })

        if not rows:
            return pd.DataFrame(columns=['ID', 'Summary', 'Start', 'End', 'Duration'])

        df = pd.DataFrame(rows)
        return Plotter._normalize_datetime_columns(df)

    @staticmethod
    def __extract_time_data(data: pd.DataFrame) -> pd.DataFrame:
        # Extract year from the Start column and convert Duration to timedelta
        data['Start'] = pd.to_datetime(data['Start'])
        data['End'] = pd.to_datetime(data['End'])
        data['Year'] = data['Start'].dt.year
        data['Month'] = data['Start'].dt.month

        # Calculate duration in hours
        data['Duration'] = pd.to_timedelta(data['End'] - data['Start']).dt.total_seconds() / 3600

        return data

    @staticmethod
    def __hours_by_summary(data):
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
        data = Plotter.__extract_time_data(data)

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
        data = Plotter.__extract_time_data(data)

        hours_by_summary = Plotter.__hours_by_summary(data)

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
        data = Plotter.__extract_time_data(data)

        hours_by_summary = Plotter.__hours_by_summary(data)

        # Create a pie chart
        plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
        hours_by_summary.plot(kind='pie', autopct='%1.1f%%', startangle=90)

        plt.xlabel('Summary', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours by Summary', fontsize=12)

        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)

        plt.legend(title='Summary', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)  # Add legend outside the plot
        ####################

    #! TODO: fix here
    @staticmethod
    def __chart4(data):
        #################### Total Hours by Summary and Year
        data = Plotter.__extract_time_data(data)

        summary_yearly_hours = data.groupby(['Year', 'Summary'])['Duration'].sum()

        # Unstack the DataFrame to have 'Summary' as columns
        summary_yearly_hours = summary_yearly_hours.unstack()

        # Plot the bar chart
        plt.figure(figsize=(12, 8))  # Adjust the figure size if needed
        summary_yearly_hours.plot(kind='bar', stacked=True)

        plt.xlabel('Year', fontsize=9)
        plt.ylabel('Total Hours', fontsize=9)
        plt.title('Total Hours by Year and Summary', fontsize=12)
        plt.legend(title='Summary', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        ####################

    @staticmethod
    def chart_total_hours_per_year(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

        yearly_hours = data.groupby('Year')['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(yearly_hours, x='Year', y='Duration', labels={'Year': 'Year', 'Duration': 'Total Hours'}, title='Total Hours per Year')

        # Add text values above the bars
        for i, row in yearly_hours.iterrows():
            fig.add_annotation(x=row['Year'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=yearly_hours['Year'], ticktext=yearly_hours['Year']))

        # Show the plot
        if not get:
            fig.show()
        else:
            return fig

    @staticmethod
    def chart_total_hours_per_month(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

        monthly_hours = data.groupby('Month')['Duration'].sum().reset_index()

        # Create a bar chart with Plotly
        fig = px.bar(monthly_hours, x='Month', y='Duration', labels={'Month': 'Month', 'Duration': 'Total Hours'}, title='Total Hours per Month')

        # Add text values above the bars
        for i, row in monthly_hours.iterrows():
            fig.add_annotation(x=row['Month'], y=row['Duration'], text=f"{row['Duration']:.2f}h", showarrow=False)

        # Customize layout
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=monthly_hours['Month'], ticktext=monthly_hours['Month']))

        # Show the plot
        if not get:
            fig.show()
        else:
            return fig
        

    @staticmethod
    def chart_total_hours_per_month_grouped_by_year(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

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
        if not get:
            fig.show()
        else:
            return fig
        ####################

    @staticmethod
    def chart_total_hours_by_summary(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

        hours_by_summary = Plotter.__hours_by_summary(data)

        # Convert Series to DataFrame
        hours_by_summary_df = pd.DataFrame({'Summary': hours_by_summary.index, 'Duration': hours_by_summary.values})

        # Create a bar chart using Plotly Express
        fig = px.bar(hours_by_summary_df, x='Summary', y='Duration', labels={'Duration': 'Total Hours'}, title='Total Hours by Summary')

        # Add text values above the bars
        for i, val in enumerate(hours_by_summary):
            fig.add_annotation(x=i, y=val + 0.05, text=f"{val:.2f}h", showarrow=False)

        # Show the plot
        if not get:
            fig.show()
        else:
            return fig
        ####################

    @staticmethod
    def chart_total_hours_by_summary_pie(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

        hours_by_summary = Plotter.__hours_by_summary(data)

        # Create a pie chart using Plotly Express
        fig = px.pie(hours_by_summary, values='Duration', names=hours_by_summary.index, labels={'Duration': 'Total Hours', 'names': 'Summary'}, title='Total Hours by Summary Pie chart')

        # Show the plot
        if not get:
            fig.show()
        else:
            return fig
        ####################

    @staticmethod
    def chart_total_hours_per_year_by_summary(data, get: bool = False):
        data = Plotter.__extract_time_data(data)

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
        if not get:
            fig.show()
        else:
            return fig
        ####################

    @staticmethod
    def chart_total_hours_per_month_by_summary(data: pd.DataFrame, get: bool = False):
        data = Plotter.__extract_time_data(data)

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
        if not get:
            fig.show()
        else:
            return fig

    @staticmethod
    def all_stats(data: pd.DataFrame):
        data = Plotter.__extract_time_data(data)

        yearly_hours = data.groupby('Year')['Duration'].sum()

        hours_by_summary = Plotter.__hours_by_summary(data)

        data.groupby(['Year', 'Summary'])['Duration'].sum().unstack()

        stats = [yearly_hours, hours_by_summary]

        # Save the full error details to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt") as temp_file:
            for stat in stats:
                temp_file.write(str(stat) + '\n\n')

        webbrowser.open(f'file://{temp_file.name}')