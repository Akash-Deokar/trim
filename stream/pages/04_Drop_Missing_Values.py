import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import base64

def display_uploaded_dataframe(df):
    st.subheader("Uploaded DataFrame:")
    st.write(df)  # Display the entire DataFrame

def calculate_missing_info(df):
    st.subheader("Missing Value Information:")
    missing_counts = df.isnull().sum()  # Count missing values in each column
    total_rows = df.shape[0]
    missing_percentages = (missing_counts / total_rows) * 100  # Calculate missing percentages for each column

    # Combine missing counts and percentages into a DataFrame
    missing_info_df = pd.DataFrame({
        'Missing Value Count': missing_counts,
        'Missing Value Percentage': missing_percentages
    })

    # Filter columns with missing value percentages between 0% and 5%
    filtered_columns = missing_info_df[
        (missing_info_df['Missing Value Percentage'] > 0) & 
        (missing_info_df['Missing Value Percentage'] < 5)
    ]

    st.write("Columns with Missing Value Percentage between 0% and 5%:")
    st.write(filtered_columns)

    return filtered_columns.index.tolist()

def filter_and_clean_dataframe(df, columns_to_clean):
    # Drop rows where selected columns have missing values within specified percentage range
    cleaned_df = df.dropna(subset=columns_to_clean)

    return cleaned_df, df

def plot_numerical_columns(df_orig, df_cleaned, numerical_columns):
    st.subheader("PDF Comparison for Numerical Columns (0% < Missing Percentage < 5%):")

    for col in numerical_columns:
        fig, ax = plt.subplots()
        sns.kdeplot(df_orig[col].dropna(), label='Original', ax=ax)
        sns.kdeplot(df_cleaned[col].dropna(), label='Cleaned', ax=ax)
        ax.set_title(f"PDF Comparison for {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Density")
        st.pyplot(fig)

def calculate_categorical_variation(df_orig, df_cleaned, categorical_columns):
    variation_data = []

    for col in categorical_columns:
        orig_value_counts = df_orig[col].value_counts()
        cleaned_value_counts = df_cleaned[col].value_counts()

        # Collect unique categories from both original and cleaned DataFrames
        unique_categories = set(orig_value_counts.index).union(set(cleaned_value_counts.index))

        # Iterate over unique categories
        for category in unique_categories:
            orig_count = orig_value_counts.get(category, 0)
            cleaned_count = cleaned_value_counts.get(category, 0)

            # Append variation data for each category in the current column
            variation_data.append({
                'Column': col,
                'Category': category,
                'Original Value Count': orig_count,
                'Cleaned Value Count': cleaned_count
            })

    # Create DataFrame from the variation data
    variation_df = pd.DataFrame(variation_data)

    return variation_df

def display_categorical_variation(variation_df):
    st.subheader("Value Counts Comparison for Categorical Columns (Old DataFrame vs Cleaned DataFrame):")
    st.write(variation_df)

def display_categorical_value_counts_percentage(df_orig, df_cleaned, categorical_columns):
    st.subheader("Value Counts as Percentages for Categorical Columns (Old vs Cleaned DataFrame):")
    
    for col in categorical_columns:
        st.write(f"Column: {col}")
        
        # Calculate value counts as percentages for original and cleaned DataFrames
        orig_value_counts_percentage = df_orig[col].value_counts(normalize=True) * 100
        cleaned_value_counts_percentage = df_cleaned[col].value_counts(normalize=True) * 100
        
        # Combine into a DataFrame for comparison
        comparison_df = pd.DataFrame({
            'Original Value Counts (%)': orig_value_counts_percentage,
            'Cleaned Value Counts (%)': cleaned_value_counts_percentage
        })
        
        st.write(comparison_df)

def download_csv(df, filename='data.csv'):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    st.title("DataFrame Analysis and Row Cleaning App")
    #df = st.session_state['df']
    # Upload a CSV file
    #uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if "df" in st.session_state:
        # Read the uploaded file into a DataFrame
        df = st.session_state.df

        # Display uploaded DataFrame
        display_uploaded_dataframe(df)

        # Calculate and filter columns based on missing value percentages (0% < missing percentage < 5%)
        columns_to_clean = calculate_missing_info(df)

        if columns_to_clean:
            # Filter and clean DataFrame based on selected columns
            cleaned_df, original_df = filter_and_clean_dataframe(df, columns_to_clean)

            # Display DataFrame shapes before and after cleaning
            st.subheader("DataFrame Shapes:")
            st.write(f"Original DataFrame Shape: {original_df.shape}")
            st.write(f"Cleaned DataFrame Shape: {cleaned_df.shape}")

            # Option to download the cleaned DataFrame
            st.subheader("Download Cleaned DataFrame:")
            download_csv(cleaned_df, filename='cleaned_data.csv')

            # Plot PDFs for numerical columns comparing original vs cleaned DataFrame
            numerical_columns = original_df.select_dtypes(include=np.number).columns.tolist()
            plot_numerical_columns(original_df, cleaned_df, numerical_columns)

            # Calculate variation in value counts for categorical columns
            categorical_columns = [col for col in columns_to_clean if df[col].dtype == 'object']  # Filter categorical columns
            variation_df = calculate_categorical_variation(original_df, cleaned_df, categorical_columns)

            # Display variation in value counts for categorical columns
            display_categorical_variation(variation_df)

            # Display value counts as percentages for categorical columns (Old vs Cleaned DataFrame)
            display_categorical_value_counts_percentage(original_df, cleaned_df, categorical_columns)
    
    else:
        st.warning("Please upload a CSV file first on the input page.")
if __name__ == "__main__":
    main()
