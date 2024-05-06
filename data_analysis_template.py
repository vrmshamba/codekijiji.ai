import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

def visualize_data_histogram(data, column):
    """
    Create a histogram for a specified column of the data.
    """
    if data is not None and column in data.columns:
        plt.hist(data[column])
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()
    else:
        print(f"Column {column} not found in data.")

def visualize_data_scatter(data, column1, column2):
    """
    Create a scatter plot for two specified columns of the data.
    """
    if data is not None and column1 in data.columns and column2 in data.columns:
        plt.scatter(data[column1], data[column2])
        plt.title(f'Scatter Plot of {column1} vs {column2}')
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.show()
    else:
        print(f"One or both columns {column1}, {column2} not found in data.")

# Main section to call functions with actual data
if __name__ == "__main__":
    # Replace 'actual_data.csv' with the path to the actual data file
    file_path = 'actual_data.csv'
    data = load_data(file_path)
    data = clean_data(data)
    # Replace 'column_name' with the actual column names
    visualize_data_histogram(data, 'column_name')
    visualize_data_scatter(data, 'column1_name', 'column2_name')
