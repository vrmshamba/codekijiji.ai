import pandas as pd
import numpy as np
import random
import string

# Function to generate random strings
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate synthetic data
def generate_synthetic_data(num_entries=1000):
    data = {
        'text_data': [random_string(random.randint(10, 100)) for _ in range(num_entries)],
        'language': [random.choice(['Kikuyu', 'Dholuo', 'Kalenjin', 'Maasai', 'Somali', 'Swahili']) for _ in range(num_entries)],
        'submitted_at': pd.date_range(start='2021-01-01', periods=num_entries, freq='H').tolist(),
        'user_id': [random.randint(1, 100) for _ in range(num_entries)]
    }
    df = pd.DataFrame(data)
    return df

# Main section to generate and save synthetic data
if __name__ == "__main__":
    synthetic_data = generate_synthetic_data()
    synthetic_data.to_csv('synthetic_data.csv', index=False)
    print("Synthetic data generated and saved to synthetic_data.csv")
