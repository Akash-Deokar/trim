import streamlit as st
import pandas as pd
import numpy as np

def calculate_z_scores_and_remove_outliers(df, selected_columns, z_thresh=3):
    """
    Calculate z-scores for selected numerical columns in the DataFrame,
    identify rows containing outliers based on the specified z-score threshold,
    and remove those rows.

    Parameters:
    df (DataFrame): Input DataFrame containing numerical columns.
    selected_columns (list): List of column names to perform outlier detection on.
    z_thresh (float): Z-score threshold for outlier detection (default=3).

    Returns:
    Tuple: A tuple containing the following:
        - df_z_scores (DataFrame): DataFrame of z-scores for selected numerical columns.
        - outlier_counts (Series): Series showing the count of outliers column-wise.
        - df_updated (DataFrame): Updated DataFrame after removing rows with outliers.
        - original_shape (Tuple): Shape (rows, columns) of the original DataFrame.
        - updated_shape (Tuple): Shape (rows, columns) of the updated DataFrame.
    """
    # Calculate z-scores for selected numerical columns
    df_z_scores = df[selected_columns].apply(lambda x: (x - x.mean()) / x.std())

    # Identify rows containing outliers based on z-score threshold
    row_outliers_mask = (np.abs(df_z_scores) > z_thresh).any(axis=1)

    # Get indices of rows containing outliers
    outlier_indices = df.index[row_outliers_mask].tolist()

    # Count outliers column-wise
    outlier_counts = (np.abs(df_z_scores) > z_thresh).sum()

    # Drop rows containing outliers from the original DataFrame
    df_updated = df[~row_outliers_mask]

    # Get shapes of original and updated DataFrames
    original_shape = df.shape
    updated_shape = df_updated.shape

    return df_z_scores, outlier_counts, df_updated, original_shape, updated_shape

def streamlit_app():
    """
    Streamlit app function to perform z-score calculation, outlier detection,
    and DataFrame manipulation by dropping entire rows containing outliers
    based on user-selected columns.
    """
    st.title('Z-Score Outlier Removal App')

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the original DataFrame
        st.subheader("Original DataFrame")
        st.write(df)

        # Checkbox or multiselect dropdown for column selection
        all_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_columns = st.multiselect("Select columns for outlier detection (Z-score)", all_columns, default=all_columns)

        if len(selected_columns) > 0:
            # User-defined z-score threshold via input box
            z_thresh = st.number_input("Z-score Threshold", value=3.0)

            # Calculate z-scores, identify and remove rows containing outliers
            df_z_scores, outlier_counts, df_updated, original_shape, updated_shape = calculate_z_scores_and_remove_outliers(df, selected_columns, z_thresh)

            # Display z-scores DataFrame
            st.subheader("Z-Scores DataFrame")
            st.write(df_z_scores)

            # Display outlier counts column-wise
            st.subheader("Outlier Counts (column-wise)")
            st.write(outlier_counts)

            # Display information about removed rows containing outliers
            if len(df) > len(df_updated):
                st.subheader("Rows with Outliers (Removed)")
                st.write(df.loc[df.index.difference(df_updated.index)])
            else:
                st.subheader("No Rows with Outliers Detected")

            # Display updated DataFrame after removing rows with outliers
            st.subheader("Updated DataFrame (after removing rows with outliers)")
            st.write(df_updated)

            # Display shapes of original and updated DataFrames
            st.subheader("DataFrame Shapes")
            st.write(f"Original DataFrame Shape: {original_shape}")
            st.write(f"Updated DataFrame Shape: {updated_shape}")
        else:
            st.warning("Please select at least one column for outlier detection (Z-score).")

if __name__ == '__main__':
    streamlit_app()
