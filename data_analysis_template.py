import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None

def clean_data(data):
    """
    Perform data cleaning operations such as handling missing values and removing duplicates.
    """
    if data is not None:
        # Handle missing values
        data = data.dropna()
        # Remove duplicates
        data = data.drop_duplicates()
        print("Data cleaned successfully.")
    return data

def visualize_data_histogram(data, column, output_path):
    """
    Create a histogram for a specified column of the data and save it as an image.
    """
    if data is not None and column in data.columns:
        sns.histplot(data[column], kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.savefig(f"{output_path}/histogram_{column}.png")
        plt.close()
        print(f"Histogram of {column} saved as histogram_{column}.png")
    else:
        print(f"Column {column} not found in data.")

def visualize_data_scatter(data, column1, column2, output_path):
    """
    Create a scatter plot for two specified columns of the data and save it as an image.
    """
    if data is not None and column1 in data.columns and column2 in data.columns:
        sns.scatterplot(x=data[column1], y=data[column2])
        plt.title(f'Scatter Plot of {column1} vs {column2}')
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.savefig(f"{output_path}/scatter_{column1}_vs_{column2}.png")
        plt.close()
        print(f"Scatter Plot of {column1} vs {column2} saved as scatter_{column1}_vs_{column2}.png")
    else:
        print(f"One or both columns {column1}, {column2} not found in data.")

# Main section to call functions with actual data
if __name__ == "__main__":
    # Replace 'actual_data.csv' with the path to the actual data file
    file_path = 'synthetic_data.csv'
    output_path = '.'  # Set the directory where the images will be saved
    data = load_data(file_path)
    data = clean_data(data)
    # Replace 'column_name' with the actual column names
    visualize_data_histogram(data, 'language', output_path)
    visualize_data_scatter(data, 'submitted_at', 'user_id', output_path)
