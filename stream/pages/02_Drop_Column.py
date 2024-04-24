import streamlit as st
import pandas as pd
import base64  # For handling file download

def main():
    st.title("Select and Display Remaining Columns")

    # Check if the DataFrame exists in session state
    if "df" in st.session_state:
        df = st.session_state.df

        # Display option to exclude non-important columns
        select_and_display_remaining_columns(df)
    else:
        st.warning("Please upload a CSV file first on the input page.")

def select_and_display_remaining_columns(df):
    st.write("### Exclude Non-Important Columns")
    st.write(df.head(5))
    # Get the list of column names from the DataFrame
    columns = df.columns.tolist()

    # Multiselect widget to choose non-important columns to exclude
    non_important_columns = st.multiselect("Select non-important columns to exclude", columns)

    if non_important_columns:
        # Exclude non-important columns to create a new DataFrame
        remaining_columns = [col for col in columns if col not in non_important_columns]
        remaining_df = df[remaining_columns]

        # Display the DataFrame with remaining columns
        st.write("### DataFrame with Remaining Columns")
        st.write(remaining_df)

        # Button to download the remaining DataFrame as CSV
        if st.button("Download Remaining DataFrame as CSV"):
            csv_file = remaining_df.to_csv(index=False)
            b64 = base64.b64encode(csv_file.encode()).decode()  # B64 encoding for CSV
            href = f'<a href="data:file/csv;base64,{b64}" download="remaining_dataframe.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
