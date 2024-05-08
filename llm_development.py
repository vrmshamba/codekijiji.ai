import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
import joblib

def load_and_preprocess_data(filepath):
    """
    Load and preprocess the dataset.
    """
    # Load the dataset
    data = pd.read_csv(filepath)

    # Preprocess the data
    # Convert language to a categorical type and encode it as an integer
    data['language'] = data['language'].astype('category')
    data['language_code'] = data['language'].cat.codes

    # We will not use 'submitted_at' and 'user_id' for the initial model training
    # However, these could be used later for more advanced models that take into account
    # the submission time and user-specific data

    # For now, we focus on the 'text_data' and 'language_code' for training the model
    # Extract features from text
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['text_data'])
    y = data['language_code']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, vectorizer

def train_model(X_train, y_train):
    """
    Train the machine learning model.
    """
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the machine learning model.
    """
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

def save_model(model, filename):
    """
    Save the trained model to a file.
    """
    joblib.dump(model, filename)

# This is a placeholder for the actual execution of the script which would
# include calls to the functions defined above with the appropriate parameters.
if __name__ == '__main__':
    filepath = 'synthetic_data.csv'  # Replace with actual data file path
    X_train, X_test, y_train, y_test, vectorizer = load_and_preprocess_data(filepath)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model, 'llm_model.joblib')  # Replace with desired output model file name
    save_model(vectorizer, 'vectorizer.joblib')  # Save the vectorizer for later use
