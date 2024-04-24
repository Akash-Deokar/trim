import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import base64

def display_uploaded_dataframe(df):
    st.subheader("Uploaded DataFrame:")
    st.write(df)  # Display the entire DataFrame

    # Get numerical columns for mean and median computation
    numerical_columns = df.select_dtypes(include=np.number).columns.tolist()

    if numerical_columns:
        # Compute mean and median for each numerical column
        summary_data = {'Column': [], 'Mean': [], 'Median': []}

        for col in numerical_columns:
            mean_value = df[col].mean()
            median_value = df[col].median()

            summary_data['Column'].append(col)
            summary_data['Mean'].append(mean_value)
            summary_data['Median'].append(median_value)

        # Create a summary DataFrame for mean and median
        summary_df = pd.DataFrame(summary_data)
        st.subheader("Mean and Median for Numerical Columns:")
        st.write(summary_df)

def identify_columns_with_missing_values(df):
    # Identify columns with missing values
    missing_columns = df.columns[df.isnull().any()].tolist()
    return missing_columns

def plot_numerical_columns_pdf(df, numerical_columns):
    st.subheader("PDF Comparison for Numerical Columns with Missing Values:")
    
    for col in numerical_columns:
        fig, ax = plt.subplots()
        sns.kdeplot(df[col].dropna(), label='Original', ax=ax)
        ax.set_title(f"PDF Comparison for {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Density")
        st.pyplot(fig)

def calculate_fill_values(df, numerical_columns):
    fill_values = {}
    for col in numerical_columns:
        mean_value = df[col].mean()
        median_value = df[col].median()
        fill_values[col] = {'Mean': mean_value, 'Median': median_value}
    return fill_values

def fill_missing_values(df, numerical_columns, fill_method='mean'):
    filled_df = df.copy()
    fill_values = calculate_fill_values(df, numerical_columns)
    
    for col in numerical_columns:
        if fill_method == 'mean':
            filled_df[col].fillna(fill_values[col]['Mean'], inplace=True)
        elif fill_method == 'median':
            filled_df[col].fillna(fill_values[col]['Median'], inplace=True)
    
    return filled_df

def calculate_numerical_variances(df, numerical_columns):
    variances = {}
    for col in numerical_columns:
        variance_value = df[col].var()
        variances[col] = variance_value
    return variances

def display_variance_comparison(original_variances, mean_filled_variances, median_filled_variances):
    st.subheader("Variance Comparison for Numerical Columns:")
    comparison_df = pd.DataFrame({
        'Column': list(original_variances.keys()),
        'Original Variance': list(original_variances.values()),
        'Mean Filled Variance': list(mean_filled_variances.values()),
        'Median Filled Variance': list(median_filled_variances.values())
    })
    st.write(comparison_df)

def display_correlation_matrix(df, title):
    st.subheader(f"Correlation Matrix ({title}):")
    
    # Filter out only numeric columns
    numeric_df = df.select_dtypes(include=np.number)
    
    # Compute correlation matrix for numeric columns
    corr_matrix = numeric_df.corr()
    
    # Display correlation matrix
    st.write(corr_matrix)

def display_covariance_matrix(df, title):
    st.subheader(f"Covariance Matrix ({title}):")
    
    # Filter out only numeric columns
    numeric_df = df.select_dtypes(include=np.number)
    
    # Compute covariance matrix for numeric columns
    cov_matrix = numeric_df.cov()
    
    # Display covariance matrix
    st.write(cov_matrix)

def plot_pdf_comparison(original_df, filled_df_mean, filled_df_median, numerical_columns):
    st.subheader("PDF Comparison: Original vs Mean Filling vs Median Filling")

    for col in numerical_columns:
        fig, ax = plt.subplots()
        sns.kdeplot(original_df[col].dropna(), label='Original', linestyle='--', ax=ax)
        sns.kdeplot(filled_df_mean[col], label='Mean Filling', ax=ax)
        sns.kdeplot(filled_df_median[col], label='Median Filling', ax=ax)
        ax.set_title(f"PDF Comparison for {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Density")
        ax.legend()  # Show legend with labels
        st.pyplot(fig)

def plot_boxplot_comparison(original_df, filled_df_mean, filled_df_median, numerical_columns):
    st.subheader("Boxplot Comparison: Original vs Mean Filling vs Median Filling")

    for col in numerical_columns:
        # Combine data for boxplot comparison
        data_to_plot = pd.DataFrame({
            'Original': original_df[col].dropna(),
            'Mean Filling': filled_df_mean[col],
            'Median Filling': filled_df_median[col]
        })

        # Create boxplot
        fig, ax = plt.subplots()
        sns.boxplot(data=data_to_plot, ax=ax, palette='Set3', width=0.5)
        ax.set_title(f"Boxplot Comparison for {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Value")
        st.pyplot(fig)

def download_link(df, filename, button_text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encoding the CSV data
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)


def main():
    st.title("DataFrame Analysis and Missing Values Handling")
    # Retrieve DataFrame from session state
    #df = st.session_state['df'] if 'df' in st.session_state else None
    if "df" in st.session_state:
        # Display uploaded DataFrame
        df = st.session_state.df
        display_uploaded_dataframe(df)

        # Identify columns with missing values
        missing_columns = identify_columns_with_missing_values(df)

        if missing_columns:
            st.subheader("Columns with Missing Values:")
            st.write(missing_columns)

            # Filter numerical columns among missing columns
            numerical_columns = df[missing_columns].select_dtypes(include=np.number).columns.tolist()

            if numerical_columns:
                # Calculate fill values (mean and median) for numerical columns
                filled_df_mean = fill_missing_values(df, numerical_columns, fill_method='mean')
                filled_df_median = fill_missing_values(df, numerical_columns, fill_method='median')

                st.subheader("Updated DataFrame after Filling Missing Values (Mean):")
                st.write(filled_df_mean)

                st.subheader("Updated DataFrame after Filling Missing Values (Median):")
                st.write(filled_df_median)

                # Add download buttons for updated DataFrames
                st.subheader("Download Updated DataFrames:")
                if st.button("Download Mean Filled DataFrame"):
                    download_link(filled_df_mean, "mean_filled_dataframe.csv", "Download Mean Filled CSV")

                if st.button("Download Median Filled DataFrame"):
                    download_link(filled_df_median, "median_filled_dataframe.csv", "Download Median Filled CSV")

                # Calculate variances of numerical columns
                original_variances = calculate_numerical_variances(df, numerical_columns)
                mean_filled_variances = calculate_numerical_variances(filled_df_mean, numerical_columns)
                median_filled_variances = calculate_numerical_variances(filled_df_median, numerical_columns)

                # Display variance comparison
                display_variance_comparison(original_variances, mean_filled_variances, median_filled_variances)

                # Display correlation matrix
                display_correlation_matrix(df, "Original DataFrame")
                display_correlation_matrix(filled_df_mean, "Updated DataFrame (Mean Filling)")
                display_correlation_matrix(filled_df_median, "Updated DataFrame (Median Filling)")

                # Display covariance matrix
                display_covariance_matrix(df, "Original DataFrame")
                display_covariance_matrix(filled_df_mean, "Updated DataFrame (Mean Filling)")
                display_covariance_matrix(filled_df_median, "Updated DataFrame (Median Filling)")

                # Plot PDF Comparison
                plot_pdf_comparison(df, filled_df_mean, filled_df_median, numerical_columns)

                # Plot Boxplot Comparison
                plot_boxplot_comparison(df, filled_df_mean, filled_df_median, numerical_columns)

                #st.write("No numerical columns with missing values found.")

        else:
            st.write("No columns with missing values found.")

    else:
        st.warning("Please upload a CSV file first on the input page.")


if __name__ == "__main__":
    main()