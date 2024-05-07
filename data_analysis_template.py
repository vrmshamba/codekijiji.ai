import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import scipy.stats as stats
import statsmodels.api as sm

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
    Create an interactive histogram for a specified column of the data and save it as an HTML file.
    """
    if data is not None and column in data.columns:
        fig = px.histogram(data, x=column)
        fig.write_html(f"{output_path}/histogram_{column}.html")
        print(f"Interactive Histogram of {column} saved as histogram_{column}.html")
    else:
        print(f"Column {column} not found in data.")

def visualize_data_scatter(data, column1, column2, output_path):
    """
    Create an interactive scatter plot for two specified columns of the data and save it as an HTML file.
    """
    if data is not None and column1 in data.columns and column2 in data.columns:
        fig = px.scatter(data, x=column1, y=column2)
        fig.write_html(f"{output_path}/scatter_{column1}_vs_{column2}.html")
        print(f"Interactive Scatter Plot of {column1} vs {column2} saved as scatter_{column1}_vs_{column2}.html")
    else:
        print(f"One or both columns {column1}, {column2} not found in data.")

def visualize_data_time_series(data, column, output_path):
    """
    Create an interactive time series plot for a specified column of the data and save it as an HTML file.
    """
    if data is not None and column in data.columns:
        fig = px.line(data, x='submitted_at', y=column)
        fig.write_html(f"{output_path}/time_series_{column}.html")
        print(f"Interactive Time Series Plot of {column} saved as time_series_{column}.html")
    else:
        print(f"Column {column} not found in data.")

def visualize_data_box(data, column, output_path):
    """
    Create an interactive box plot for a specified column of the data and save it as an HTML file.
    """
    if data is not None and column in data.columns:
        fig = px.box(data, y=column)
        fig.write_html(f"{output_path}/box_plot_{column}.html")
        print(f"Interactive Box Plot of {column} saved as box_plot_{column}.html")
    else:
        print(f"Column {column} not found in data.")

def visualize_correlation_matrix(data, output_path):
    """
    Create an interactive correlation matrix heatmap for the data and save it as an HTML file.
    """
    if data is not None:
        # Select only numeric columns for correlation matrix
        numeric_data = data.select_dtypes(include=[np.number])
        fig = ff.create_annotated_heatmap(
            z=numeric_data.corr().values,
            x=list(numeric_data.columns),
            y=list(numeric_data.columns),
            annotation_text=numeric_data.corr().round(2).values,
            showscale=True
        )
        fig.write_html(f"{output_path}/correlation_matrix.html")
        print("Interactive Correlation Matrix saved as correlation_matrix.html")
    else:
        print("Data is not available for correlation matrix.")

def summarize_data(data):
    """
    Generate summary statistics for the data.
    """
    if data is not None:
        summary = data.describe()
        print("Summary statistics generated.")
        return summary
    else:
        print("Data is not available for summary statistics.")
        return None

def perform_linear_regression(data, independent_var, dependent_var):
    """
    Perform simple linear regression analysis on two specified columns of the data.
    """
    if data is not None and independent_var in data.columns and dependent_var in data.columns:
        X = sm.add_constant(data[independent_var])  # adding a constant
        model = sm.OLS(data[dependent_var], X).fit()
        predictions = model.predict(X)
        print_model = model.summary()
        print(print_model)
    else:
        print(f"One or both columns {independent_var}, {dependent_var} not found in data.")

def perform_multiple_regression(data, independent_vars, dependent_var):
    """
    Perform multiple regression analysis on specified independent variables and a single dependent variable.
    """
    if data is not None and all(var in data.columns for var in independent_vars) and dependent_var in data.columns:
        X = sm.add_constant(data[independent_vars])  # adding a constant
        model = sm.OLS(data[dependent_var], X).fit()
        print(model.summary())
    else:
        print(f"Some columns specified for multiple regression not found in data.")

def perform_logistic_regression(data, independent_vars, dependent_var):
    """
    Perform logistic regression analysis on specified independent variables and a binary dependent variable.
    """
    if data is not None and all(var in data.columns for var in independent_vars) and dependent_var in data.columns:
        X = sm.add_constant(data[independent_vars])  # adding a constant
        model = sm.Logit(data[dependent_var], X).fit()
        print(model.summary())
    else:
        print(f"Some columns specified for logistic regression not found in data.")

def perform_hypothesis_testing(data, column1, column2):
    """
    Perform hypothesis testing between two specified columns of the data.
    """
    if data is not None and column1 in data.columns and column2 in data.columns:
        stat, p_value = stats.ttest_ind(data[column1], data[column2])
        print(f"T-test result for {column1} and {column2}: Statistic={stat}, P-value={p_value}")
    else:
        print(f"One or both columns {column1}, {column2} not found in data for hypothesis testing.")

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
    visualize_data_time_series(data, 'submitted_at', output_path)
    visualize_data_box(data, 'user_id', output_path)
    visualize_correlation_matrix(data, output_path)
    summary_stats = summarize_data(data)
    print(summary_stats)
