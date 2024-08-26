import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from io import BytesIO

# load dataset
def load_data(upload_file):
  data=pd.read_excel(upload_file)
  return data

def stratified_split(data, n_split):
  # Hold out 10% of the data for global model testing
  train_data, test_data = train_test_split(
        data, test_size=0.1, stratify=data['Type of attack'], random_state=seed
    )
  # Remaining data for client splits
  remaining_data = train_data
  data_splits = []

  for i in range(n_split - 1):
      split, remaining_data = train_test_split(
          remaining_data, test_size=1/(n_split - i), stratify=remaining_data['Type of attack'], random_state=42
        )
      data_splits.append(split)

  data_splits.append(remaining_data)

  return data_splits, test_data

# Analyze splits
def analyze_splits(splits, test_data):
    buffers = []
    for i, split in enumerate(splits):
        st.write(f"Client {i+1} data shape:", split.shape)
        st.write(f"Client {i+1} data distribution:\n", split["Type of attack"].value_counts())

        # Visualize class distribution
        fig, ax = plt.subplots()
        split["Type of attack"].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f'Client {i+1} class distribution')
        st.pyplot(fig)

        # Statistical summary
        st.write(f"Client {i+1} statistical summary")
        st.write(split.describe())

        # Visualize feature distribution
        numerical_features = split.select_dtypes(include=['int64', 'float64']).columns
        for feature in numerical_features:
            fig, ax = plt.subplots()
            sns.histplot(split[feature], kde=True, ax=ax)
            ax.set_title(f'Client {i+1} {feature} distribution')
            st.pyplot(fig)

        # Check for missing values
        st.write(f"Client {i+1} Missing Values")
        st.write(split.isnull().sum())

        # Prepare download link for the split file
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            split.to_excel(writer, index=False, sheet_name='Sheet1')
        buffers.append((f"Download Client {i+1} data as Excel", buffer))

    # Analyze the global test set
    st.write("Global model test data shape:", test_data.shape)
    st.write("Global model test data distribution:\n", test_data["Type of attack"].value_counts())

    fig, ax = plt.subplots()
    test_data["Type of attack"].value_counts().plot(kind='bar', ax=ax)
    ax.set_title('Global model test data class distribution')
    st.pyplot(fig)

    # Statistical summary for the global test set
    st.write("Global model test data statistical summary")
    st.write(test_data.describe())

    # Visualize feature distribution for the global test set
    for feature in numerical_features:
        fig, ax = plt.subplots()
        sns.histplot(test_data[feature], kde=True, ax=ax)
        ax.set_title(f'Global model test data {feature} distribution')
        st.pyplot(fig)

    # Check for missing values in the global test set
    st.write("Global model test data Missing Values")
    st.write(test_data.isnull().sum())

    # Prepare download link for the global test data
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        test_data.to_excel(writer, index=False, sheet_name='Sheet1')
    buffers.append(("Download Global model test data as Excel", buffer))

    # Provide all download links
    for label, buffer in buffers:
        st.download_button(
            label=label,
            data=buffer.getvalue(),
            file_name=f"{label.split()[1].lower()}_data.xlsx",
            mime="application/vnd.ms-excel"
        )

# Streamlit app
def main():
    st.title("ECU-IoHT Data Splitter and Analyzer")

    # File uploader
    upload_file = st.file_uploader("Upload your data file (Excel file)", type=["xlsx"])

    if upload_file is not None:
        data = load_data(upload_file)
        st.write("Data Shape:", data.shape)
        st.write("Class distribution:", data["Type of attack"].value_counts())

        n_split = st.number_input("Enter the number of splits:", min_value=2, max_value=10, value=3)

        if st.button("Perform stratified split"):
            splits, test_data = stratified_split(data, n_split)
            for i, split in enumerate(splits):
                split_file_path = f"client_{i+1}_data.xlsx"
                split.to_excel(split_file_path, index=False)
                st.write(f"Client {i+1} data saved to {split_file_path}")

            analyze_splits(splits, test_data)

if __name__ == "__main__":
    main()
