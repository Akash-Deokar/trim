import streamlit as st
import pandas as pd

def drop_rows_by_indices(df, indices_to_drop):
    """
    Drop rows from the DataFrame based on user-provided indices.
    """
    try:
        indices_to_drop = [int(idx) for idx in indices_to_drop.split(',') if idx.strip().isdigit()]
        df_dropped = df.drop(index=indices_to_drop).reset_index(drop=True)
        return df_dropped
    except ValueError:
        st.warning("Please enter valid row indices to drop (comma-separated integers).")
        return df

def drop_rows_by_value(df, column_name, value_to_drop):
    """
    Drop rows from the DataFrame based on a specific value in a given column.
    """
    try:
        df_dropped = df[df[column_name] != value_to_drop].reset_index(drop=True)
        return df_dropped
    except KeyError:
        st.warning("Please select a valid column.")
        return df

def main():
    st.title("DataFrame Row Dropping App")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)

        st.header("Original DataFrame")
        st.write(df)

        # Sidebar options for row dropping
        st.sidebar.subheader("Drop Rows by Indices")
        indices_to_drop = st.sidebar.text_input("Enter row indices to drop (comma-separated)", "")

        st.sidebar.subheader("Drop Rows by Value in Column")
        column_options = df.columns.tolist()
        column_name = st.sidebar.selectbox("Select column for value-based dropping", column_options)
        value_to_drop = st.sidebar.text_input(f"Enter value to drop in column '{column_name}'", "")

        if indices_to_drop:
            # Drop rows by specified indices
            df = drop_rows_by_indices(df, indices_to_drop)
            st.header("Updated DataFrame after Dropping Rows by Indices")
            st.write(df)

        if column_name and value_to_drop:
            # Drop rows based on value in a specific column
            df = drop_rows_by_value(df, column_name, value_to_drop)
            st.header("Updated DataFrame after Dropping Rows by Value")
            st.write(df)

if __name__ == "__main__":
    main()
