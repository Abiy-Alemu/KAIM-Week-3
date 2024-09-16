import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind
import os

def generate_insurance_data(num_records=1000):
    """
    Generate random insurance data with provinces, gender, and claims.
    The claim rates are varied across provinces and genders to ensure significant differences.
    
    Parameters:
    num_records (int): Number of records to generate. Default is 1000.
    
    Returns:
    pd.DataFrame: Generated insurance data with columns ['Province', 'Gender', 'Claimed'].
    """
    np.random.seed(42)  # Ensures reproducibility of random data
    provinces = ['Province_A', 'Province_B', 'Province_C']  # List of provinces
    genders = ['Male', 'Female']  # List of genders
    
    # Define different claim rates for each province (to ensure statistical significance)
    claim_rates_province = {
        'Province_A': 0.1,  # 10% claim rate
        'Province_B': 0.9,  # 90% claim rate
        'Province_C': 0.2   # 20% claim rate
    }
    
    # Define different claim rates for each gender
    claim_rates_gender = {
        'Male': 0.6,   # 60% claim rate for males
        'Female': 0.2  # 20% claim rate for females
    }
    
    # Randomly assign a province to each record
    province_choices = np.random.choice(provinces, num_records)
    
    # Randomly assign a gender to each record
    gender_choices = np.random.choice(genders, num_records)
    
    # Generate 'Claimed' (0 or 1) based on gender-specific claim rates
    claims = [1 if np.random.rand() < claim_rates_gender[gender] else 0 for gender in gender_choices]
    
    # Create a DataFrame with the generated data
    data = {
        'Province': province_choices,
        'Gender': gender_choices,
        'Claimed': claims
    }
    
    return pd.DataFrame(data)

def save_data_to_csv(data, filename='insurance_data.csv'):
    """
    Save the generated insurance data to a CSV file in a specific directory.
    
    Parameters:
    data (pd.DataFrame): The insurance data to save.
    filename (str): The name of the CSV file to save the data. Default is 'insurance_data.csv'.
    """
    # Directory where the CSV file will be saved
    save_path = r'C:\Users\MMM\Documents\10 Academy File\AB Hypothesis Testing\AB Hypothesis Testing\data'
    
    # Create the directory if it doesn't already exist
    os.makedirs(save_path, exist_ok=True)
    
    # Save the DataFrame as a CSV file without the index
    data.to_csv(os.path.join(save_path, filename), index=False)

def preprocessing_script(data):
    """
    Perform Chi-squared test to check if there's a significant difference in claim rates across provinces.
    
    Parameters:
    data (pd.DataFrame): The insurance data containing 'Province' and 'Claimed' columns.
    
    Returns:
    chi2 (float): Chi-squared statistic.
    p (float): p-value of the test.
    contingency_table (pd.DataFrame): Contingency table used for the Chi-squared test.
    """
    # Create a contingency table with Province as rows and Claimed as columns
    contingency_table = pd.crosstab(data['Province'], data['Claimed'])
    
    # Perform the Chi-squared test based on the contingency table
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    return chi2, p, contingency_table

def gender_analysis(data):
    """
    Perform t-test analysis to compare claim rates between males and females.
    
    Parameters:
    data (pd.DataFrame): The insurance data containing 'Gender' and 'Claimed' columns.
    
    Returns:
    t_stat (float): T-statistic for the t-test.
    p_value (float): p-value for the t-test.
    """
    # Filter the 'Claimed' column for males and females separately
    male_claims = data[data['Gender'] == 'Male']['Claimed']
    female_claims = data[data['Gender'] == 'Female']['Claimed']
    
    # Perform an independent t-test between male and female claim rates
    t_stat, p_value = ttest_ind(male_claims, female_claims, equal_var=False)
    
    return t_stat, p_value

def save_insurance_data_to_csv(text_file_path, csv_file_name='insurance_text_data.csv'):
    """
    Convert pipe-delimited insurance data from a text file into a CSV file.
    
    Parameters:
    text_file_path (str): The path to the pipe-delimited text file.
    csv_file_name (str): The name of the CSV file to save the converted data. Default is 'insurance_text_data.csv'.
    """
    # Read the text file as a DataFrame, assuming it's pipe-delimited ('|')
    df = pd.read_csv(text_file_path, delimiter='|')
    
    # Directory where the CSV file will be saved
    save_path = r'C:\Users\MMM\Documents\10 Academy File\AB Hypothesis Testing\AB Hypothesis Testing\data'
    
    # Create the directory if it doesn't already exist
    os.makedirs(save_path, exist_ok=True)

    # Define the full file path for saving the CSV
    csv_file_path = os.path.join(save_path, csv_file_name)
    
    # Save the DataFrame to a CSV file without the index
    df.to_csv(csv_file_path, index=False)

    print(f"Data saved to {csv_file_path}")

# # Example usage:
# if __name__ == "__main__":
#     # Define the path to the pipe-delimited text file
#     text_file_path = r'C:\Users\MMM\Documents\10 Academy File\MachineLearningRating_v3.txt'
    
#     # Save the insurance data from the text file to a CSV
#     save_insurance_data_to_csv(text_file_path)
    
#     # Generate random insurance data
#     insurance_data = generate_insurance_data()

#     # Save the generated data to a CSV file
#     save_data_to_csv(insurance_data)

#     # Perform Chi-squared test for provinces
#     chi2_stat, p_value, contingency_table = preprocessing_script(insurance_data)
#     print("Chi-squared Statistic:", chi2_stat)
#     print("P-value (Provinces):", p_value)
#     print("Contingency Table (Provinces):\n", contingency_table)

#     # Perform t-test for gender analysis
#     t_stat, gender_p_value = gender_analysis(insurance_data)
#     print("T-statistic (Gender):", t_stat)
#     print("P-value (Gender):", gender_p_value)
