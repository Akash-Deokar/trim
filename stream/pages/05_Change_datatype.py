import streamlit as st
import pandas as pd

def main():
    st.title("CSV Data Type Converter")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original DataFrame")
        st.write(df)

        st.sidebar.subheader("Select Columns and Data Types")
        selected_cols = st.sidebar.multiselect("Choose columns to convert", df.columns.tolist())

        if selected_cols:
            # Display data type selection for each selected column
            data_type_selection = {}
            for col in selected_cols:
                data_type_selection[col] = st.sidebar.selectbox(f"Select data type for column '{col}'", ["int", "float", "object"])

            if st.sidebar.button("Convert Selected Columns"):
                try:
                    df_selected = df.copy()  # Create a copy of the original DataFrame

                    # Data type information before conversion
                    original_data_types = df_selected[selected_cols].dtypes

                    # Convert selected columns to the chosen data types
                    for col in selected_cols:
                        new_data_type = get_data_type(data_type_selection[col])
                        if new_data_type is not None:
                            df_selected[col] = df_selected[col].astype(new_data_type)

                    st.header("DataFrame after Data Type Conversion")
                    st.write(df_selected)

                    # Data type information after conversion
                    new_data_types = df_selected[selected_cols].dtypes

                    # Display data type information before and after conversion
                    st.subheader("Data Types Before Conversion")
                    st.write(original_data_types)

                    st.subheader("Data Types After Conversion")
                    st.write(new_data_types)

                except Exception as e:
                    st.error(f"Error occurred during data type conversion: {e}")

def get_data_type(data_type):
    """
    Get the corresponding data type based on the user-selected option.
    """
    if data_type == "int":
        return "int"
    elif data_type == "float":
        return "float"
    elif data_type == "object":
        return "str"
    else:
        return None

if __name__ == "__main__":
    main()
