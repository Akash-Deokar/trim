import streamlit as st
import pandas as pd
from sklearn.preprocessing import RobustScaler

def scale_numerical_columns(df):
    """
    Scale numerical columns (float and int) in the DataFrame using RobustScaler.
    """
    # Identify numerical columns
    numerical_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

    if not numerical_cols:
        st.warning("No numerical columns found in the DataFrame.")
        return df

    # Perform Robust Scaling using RobustScaler
    scaler = RobustScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    return df

def main():
    st.title("DataFrame Robust Scaling App")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original DataFrame")
        st.write(df)

        # Perform Robust Scaling on numerical columns
        df_scaled = scale_numerical_columns(df.copy())

        st.header("Updated DataFrame after Robust Scaling")
        st.write(df_scaled)

        # Button to download updated DataFrame as CSV
        st.sidebar.markdown("---")
        st.sidebar.header("Download Updated CSV")
        st.sidebar.download_button(
            label="Download CSV",
            data=df_scaled.to_csv(index=False),
            file_name="updated_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
