import streamlit as st
import pandas as pd

def replace_outliers_iqr(df, selected_columns):
    """
    Replace outliers based on the Interquartile Range (IQR) method.

    Parameters:
    df (DataFrame): Input DataFrame containing numerical columns.
    selected_columns (list): List of column names to perform outlier replacement on.

    Returns:
    Tuple: A tuple containing the following:
        - df_replaced (DataFrame): DataFrame with outliers replaced within the IQR limits.
        - outlier_counts (Series): Series showing the count of outliers for each selected column.
        - replaced_df (DataFrame): DataFrame containing rows with replaced outlier values.
        - original_shape (Tuple): Shape (rows, columns) of the original DataFrame.
        - replaced_shape (Tuple): Shape (rows, columns) of the DataFrame after replacing outliers.
    """
    df_replaced = df.copy()
    outlier_counts = pd.Series(0, index=selected_columns)  # Initialize outlier counts for selected columns
    replaced_df = pd.DataFrame()  # Initialize DataFrame for replaced rows
    
    # Calculate quartiles (Q1 and Q3) for each selected numeric column
    quartiles = df[selected_columns].quantile([0.25, 0.75])
    Q1 = quartiles.loc[0.25]
    Q3 = quartiles.loc[0.75]
    
    # Calculate Interquartile Range (IQR) for each selected numeric column
    IQR = Q3 - Q1
    
    # Determine outlier boundaries for each selected numeric column using IQR method
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    
    # Replace outliers within the IQR limits for each selected numeric column
    for col in selected_columns:
        # Replace values below the lower limit with the lower limit value
        df_replaced[col] = df_replaced[col].apply(lambda x: lower_limit[col] if x < lower_limit[col] else x)
        
        # Replace values above the upper limit with the upper limit value
        df_replaced[col] = df_replaced[col].apply(lambda x: upper_limit[col] if x > upper_limit[col] else x)
        
        # Count outliers replaced for the current column
        outlier_counts[col] = ((df[col] < lower_limit[col]) | (df[col] > upper_limit[col])).sum()
        
        # Identify and store replaced rows for the current column
        replaced_rows = df[((df[col] < lower_limit[col]) | (df[col] > upper_limit[col]))]
        replaced_df = pd.concat([replaced_df, replaced_rows])
    
    # Get shapes of original and replaced DataFrames
    original_shape = df.shape
    replaced_shape = df_replaced.shape
    
    return df_replaced, outlier_counts, replaced_df, original_shape, replaced_shape

def main():
    st.title('Replace Outliers with IQR Method')
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        st.write("### Original Data")
        df = pd.read_csv(uploaded_file)
        st.write(df)
        
        # Checkbox or multiselect dropdown for column selection
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns for outlier replacement", all_columns, default=all_columns)
        
        if len(selected_columns) > 0:
            # Replace outliers using IQR for selected columns
            try:
                replaced_df, outlier_counts, replaced_rows, original_shape, replaced_shape = replace_outliers_iqr(df, selected_columns)
                
                st.write("### Data after Replacing Outliers (IQR Method)")
                st.write(replaced_df)
                
                # Display replaced rows (Rows with replaced outliers)
                if not replaced_rows.empty:
                    st.write("### Replaced Rows (Rows with Outliers Replaced)")
                    st.write(replaced_rows)
                
                # Display outlier counts per selected column
                st.write("### Outlier Counts (Column-wise)")
                st.write(outlier_counts)
                
                # Display shape information
                st.write("### DataFrame Shapes")
                st.write(f"Original DataFrame Shape: {original_shape}")
                st.write(f"Replaced DataFrame Shape: {replaced_shape}")
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please select at least one column for outlier replacement.")

if __name__ == "__main__":
    main()
