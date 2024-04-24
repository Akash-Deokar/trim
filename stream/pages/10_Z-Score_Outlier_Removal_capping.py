import streamlit as st
import pandas as pd
import numpy as np

def apply_capping(df, selected_columns):
    """
    Apply capping to selected numerical columns in the DataFrame.
    Outliers are replaced with values within the specified range based on z-scores.

    Parameters:
    df (DataFrame): Input DataFrame containing numerical columns.
    selected_columns (list): List of column names to apply capping on.

    Returns:
    Tuple: A tuple containing the following:
        - df_capped (DataFrame): DataFrame with outliers in selected numerical columns replaced within the specified range.
        - excluded_indices (List): List of indices corresponding to rows containing outliers.
        - outlier_counts (Series): Series showing the count of excluded rows (outliers) column-wise.
    """
    df_capped = df.copy()
    excluded_indices = []
    outlier_counts = pd.Series(0, index=df.columns)  # Initialize outlier counts

    for col in selected_columns:
        # Calculate mean and standard deviation of the column
        mean_col = df_capped[col].mean()
        std_col = df_capped[col].std()

        # Calculate upper and lower limits for capping based on z-scores (3 standard deviations)
        upper_limit = mean_col + 3 * std_col
        lower_limit = mean_col - 3 * std_col

        # Identify outliers (rows to be excluded)
        outlier_mask = (df_capped[col] > upper_limit) | (df_capped[col] < lower_limit)
        excluded_indices.extend(df_capped[outlier_mask].index.tolist())

        # Update outlier counts for the current column
        outlier_counts[col] = sum(outlier_mask)

        # Apply capping to the column
        df_capped[col] = np.where(df_capped[col] > upper_limit, upper_limit,
                                  np.where(df_capped[col] < lower_limit, lower_limit, df_capped[col]))

    return df_capped, excluded_indices, outlier_counts

def streamlit_app():
    """
    Streamlit app function to apply capping on selected numerical columns within a DataFrame.
    """
    st.title('Capping Outliers in Numerical Columns')
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the original DataFrame
        st.subheader("Original DataFrame")
        st.write(df)
        
        # Checkbox or multiselect dropdown for column selection
        all_numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_columns = st.multiselect("Select columns for outlier capping", all_numeric_columns, default=all_numeric_columns)

        if len(selected_columns) > 0:
            # Apply capping to selected numerical columns
            df_capped, excluded_indices, outlier_counts = apply_capping(df, selected_columns)
        
            # Display DataFrame after applying capping
            st.subheader("DataFrame after Capping Outliers in Selected Columns")
            st.write(df_capped)
            
            # Display shapes of original and capped DataFrames
            st.subheader("DataFrame Shapes")
            st.write(f"Original DataFrame Shape: {df.shape}")
            st.write(f"Capped DataFrame Shape: {df_capped.shape}")
            
            # Display excluded rows (rows containing outliers)
            if len(excluded_indices) > 0:
                st.subheader("Excluded Rows (Containing Outliers)")
                st.write(df.loc[excluded_indices])
            else:
                st.subheader("No Rows Excluded (No Outliers Detected)")
            
            # Display column-wise outlier counts
            st.subheader("Column-wise Outlier Counts")
            st.write(outlier_counts)
        else:
            st.warning("Please select at least one numerical column for outlier capping.")

if __name__ == '__main__':
    streamlit_app()
