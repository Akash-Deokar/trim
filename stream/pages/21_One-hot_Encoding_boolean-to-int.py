import streamlit as st
import pandas as pd

def convert_boolean_to_int(df):
    """
    Convert boolean values (True/False) in the DataFrame to integer representations (1/0).
    """
    # Identify columns with boolean dtype
    boolean_cols = df.select_dtypes(include='bool').columns
    
    # Convert boolean columns to integer (1 for True, 0 for False)
    df[boolean_cols] = df[boolean_cols].astype(int)
    
    return df

def main():
    st.title("Convert Boolean Values to Integer (1/0) App")
    st.subheader("Upload downloaded file of one-hot encoding to convert boolean to binary")
    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a boolean file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original Data")
        st.write(df)

        # Convert boolean values to integer (1/0)
        df_updated = convert_boolean_to_int(df.copy())

        st.header("Updated Data with Boolean Conversion")
        st.write(df_updated)

        # Button to download updated DataFrame as CSV
        st.sidebar.markdown("---")
        st.sidebar.header("Download Updated CSV")
        st.sidebar.download_button(
            label="Download CSV",
            data=df_updated.to_csv(index=False),
            file_name="updated_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
