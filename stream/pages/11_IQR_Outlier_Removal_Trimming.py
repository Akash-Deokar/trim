import streamlit as st
import pandas as pd

def remove_outlier_rows_iqr(df, selected_columns):
    """
    Remove rows with outliers based on the Interquartile Range (IQR) method for specified columns.

    Parameters:
    df (DataFrame): Input DataFrame containing numerical columns.
    selected_columns (list): List of column names to perform outlier removal on.

    Returns:
    Tuple: A tuple containing the following:
        - df_updated (DataFrame): Updated DataFrame after removing rows with outliers.
        - excluded_rows (DataFrame): DataFrame containing rows with outliers.
        - outlier_counts (Series): Series showing the count of outliers for each selected column.
        - original_shape (Tuple): Shape (rows, columns) of the original DataFrame.
        - updated_shape (Tuple): Shape (rows, columns) of the updated DataFrame.
    """
    df_updated = df.copy()
    outlier_counts = pd.Series(0, index=selected_columns)  # Initialize outlier counts for selected columns
    excluded_rows = []  # List to store rows with outliers

    # Calculate quartiles (Q1 and Q3) for each selected numeric column
    quartiles = df[selected_columns].quantile([0.25, 0.75])
    Q1 = quartiles.loc[0.25]
    Q3 = quartiles.loc[0.75]

    # Calculate Interquartile Range (IQR) for each selected numeric column
    IQR = Q3 - Q1

    # Determine outlier boundaries for each selected numeric column using IQR method
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Iterate over each row
    for idx, row in df.iterrows():
        # Check if any numeric column value in the row is an outlier within selected columns
        is_outlier_row = False
        for col in selected_columns:
            # Check if current row's value in the column is an outlier
            if row[col] < lower_limit[col] or row[col] > upper_limit[col]:
                is_outlier_row = True
                outlier_counts[col] += 1  # Increment outlier count for the column
                excluded_rows.append(row)  # Store the entire row as an excluded row
                break

        # If the row contains any outlier in selected columns, mark the index for removal
        if is_outlier_row:
            df_updated.drop(idx, inplace=True)

    # Convert list of excluded rows to a DataFrame
    excluded_df = pd.DataFrame(excluded_rows, columns=df.columns)

    # Get shapes of original and updated DataFrames
    original_shape = df.shape
    updated_shape = df_updated.shape

    return df_updated, excluded_df, outlier_counts, original_shape, updated_shape

def main():
    st.title('Remove Rows with Outliers')

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        st.write("### Original Data")
        df = pd.read_csv(uploaded_file)
        st.write(df)

        # Checkbox or multiselect dropdown for column selection
        all_columns = df.select_dtypes(include=['number']).columns.tolist()
        selected_columns = st.multiselect("Select columns for outlier removal (IQR Method)", all_columns, default=all_columns)

        if len(selected_columns) > 0:
            # Remove rows with outliers using IQR for selected columns
            try:
                cleaned_df, excluded_df, outlier_counts, original_shape, updated_shape = remove_outlier_rows_iqr(df, selected_columns)

                st.write("### Data after Removing Rows with Outliers")
                st.write(cleaned_df)

                # Display excluded rows (Rows with outliers)
                if not excluded_df.empty:
                    st.write("### Excluded Rows (Rows with Outliers)")
                    st.write(excluded_df)

                # Display outlier counts per selected column
                st.write("### Outlier Counts (Column-wise)")
                st.write(outlier_counts)

                # Display shape information
                st.write(f"Original Data Shape: {original_shape}")
                st.write(f"Cleaned Data Shape: {updated_shape}")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please select at least one column for outlier removal.")

if __name__ == "__main__":
    main()
