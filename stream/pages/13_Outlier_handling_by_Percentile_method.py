import streamlit as st
import pandas as pd
import numpy as np

def trim_and_cap_outliers(df, selected_columns, lower_percentile, upper_percentile):
    """
    Trim rows containing outliers and cap outlier values within custom percentile ranges for specified columns.

    Parameters:
    df (DataFrame): Input DataFrame containing numerical columns.
    selected_columns (list): List of column names to perform outlier trimming and capping on.
    lower_percentile (float): Lower percentile value (e.g., 0.1 for 0.1th percentile).
    upper_percentile (float): Upper percentile value (e.g., 99.9 for 99.9th percentile).

    Returns:
    Tuple: A tuple containing the following:
        - trimmed_df (DataFrame): DataFrame after trimming rows with outliers.
        - capped_df (DataFrame): DataFrame with outlier values capped within specified percentiles.
    """
    df_processed = df.copy()

    # Calculate lower and upper bounds based on custom percentiles for selected columns
    lower_limit = df[selected_columns].quantile(lower_percentile / 100)
    upper_limit = df[selected_columns].quantile(upper_percentile / 100)

    # Identify rows containing outliers and trim them for selected columns
    row_outliers_mask = ((df_processed[selected_columns] < lower_limit) | (df_processed[selected_columns] > upper_limit)).any(axis=1)
    trimmed_df = df_processed[~row_outliers_mask]

    # Cap outlier values within the specified percentile limits for selected columns
    for col in selected_columns:
        df_processed[col] = np.where(df_processed[col] < lower_limit[col], lower_limit[col], df_processed[col])
        df_processed[col] = np.where(df_processed[col] > upper_limit[col], upper_limit[col], df_processed[col])

    capped_df = df_processed

    return trimmed_df, capped_df

def display_dataframe_shapes(original_shape, trimmed_shape, capped_shape):
    """
    Display the shapes (number of rows and columns) of original, trimmed, and capped DataFrames.

    Parameters:
    original_shape (Tuple): Shape (rows, columns) of the original DataFrame.
    trimmed_shape (Tuple): Shape (rows, columns) of the trimmed DataFrame.
    capped_shape (Tuple): Shape (rows, columns) of the capped DataFrame.
    """
    st.write("### DataFrame Shapes")
    st.write(f"Original DataFrame Shape: {original_shape}")
    st.write(f"Trimmed DataFrame Shape: {trimmed_shape}")
    st.write(f"Capped DataFrame Shape: {capped_shape}")

def main():
    st.title('Outlier Trimming and Capping App')

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write("### Original Data")
        st.write(df)

        # Checkbox or multiselect dropdown for column selection
        all_columns = df.select_dtypes(include=['number']).columns.tolist()
        selected_columns = st.multiselect("Select columns for outlier trimming and capping", all_columns, default=all_columns)

        if len(selected_columns) > 0:
            # User-defined percentiles via input boxes
            lower_percentile = st.number_input("Lower Percentile (e.g., 0.1 for 0.1th percentile)", min_value=0.0, max_value=100.0, value=0.1, step=0.1)
            upper_percentile = st.number_input("Upper Percentile (e.g., 99.9 for 99.9th percentile)", min_value=0.0, max_value=100.0, value=99.9, step=0.1)

            # Trim and cap outliers using custom percentiles for selected columns
            try:
                trimmed_df, capped_df = trim_and_cap_outliers(df, selected_columns, lower_percentile, upper_percentile)

                st.write("### Data after Trimming Outliers")
                st.write(trimmed_df)

                st.write("### Data after Capping Outliers")
                st.write(capped_df)

                # Display dataframe shapes
                display_dataframe_shapes(df.shape, trimmed_df.shape, capped_df.shape)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please select at least one column for outlier trimming and capping.")

if __name__ == "__main__":
    main()
