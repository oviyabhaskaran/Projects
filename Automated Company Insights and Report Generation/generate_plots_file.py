import os
import pandas as pd
import matplotlib.pyplot as plt
from functionality.process_input_file import process_input_excel_to_output

def generate_plots1(df):
    # Remove rows with NaN values in the 'Company Name' column
    df_cleaned = df.dropna(subset=['Company Name'])
    # Group by the company name
    grouped = df_cleaned.groupby('Company Name')

    # Generate plots for each group
    output_plot_directory1 = "output_plot_directory1"
    for name, group in grouped:
        # Plot data for each group
        fig, ax = plt.subplots(figsize=(10, 6))
        for metric in group['Metrics'].unique():
            metric_data = group[group['Metrics'] == metric].iloc[:, 3:-5]

            # Check if the 'Unit' column is present and the unit is not 'Percentage'
            if 'Unit' in metric_data.columns and metric_data['Unit'].iloc[0] != 'Percentage':
                for index, row in metric_data.iterrows():
                    ax.plot(row.index, row.values, marker='o', label=metric)
                    for i, value in enumerate(row.values):
                        ax.annotate(f'{value}', (row.index[i], value),
                                    textcoords="offset points",
                                    xytext=(0,10),
                                    ha='center')

        ax.set_xlabel('Date')
        ax.set_ylabel(f'Value (Crores/Billions/Millions)')
        ax.set_title(f'{name} - Overall Performance')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        plt.tight_layout()

        try:
            if not os.path.exists(output_plot_directory1):
                os.makedirs(output_plot_directory1)
        except OSError as e:
            print(f"Error: {e.strerror}")

        # Save the plot image to a file
        output_plot_path = os.path.join(output_plot_directory1, f'{name}.png')
        plt.savefig(output_plot_path)

    return output_plot_directory1

def generate_plots2(df):
    # Remove rows with NaN values in the 'Company Name' column
    df_cleaned = df.dropna(subset=['Company Name'])
    # Group by the company name
    grouped = df_cleaned.groupby('Company Name')

    # Generate plots for each group
    output_plot_directory2 = "output_plot_directory2"
    for name, group in grouped:
        # Plot data for each group
        fig, ax = plt.subplots(figsize=(10, 6))
        for metric in group['Metrics'].unique():
            metric_data = group[group['Metrics'] == metric].iloc[:, 3:-5]
            # Check if the 'Unit' column is present and the unit is 'Percentage'
            if 'Unit' in metric_data.columns and metric_data['Unit'].iloc[0] == 'Percentage':
                for index, row in metric_data.iterrows():
                    ax.plot(row.index, row.values, marker='o', label=metric)
                    for i, value in enumerate(row.values):
                        ax.annotate(f'{value}', (row.index[i], value),
                                    textcoords="offset points",
                                    xytext=(0,10),
                                    ha='center')
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Value (Percentage)')
        ax.set_title(f'{name} - Overall Performance')
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        plt.tight_layout()

        try:
            if not os.path.exists(output_plot_directory2):
                os.makedirs(output_plot_directory2)
        except OSError as e:
            print(f"Error: {e.strerror}")

        # Save the plot image to a file
        output_plot_path = os.path.join(output_plot_directory2, f'{name}.png')
        plt.savefig(output_plot_path)

    return output_plot_directory2
