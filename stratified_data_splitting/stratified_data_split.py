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
  data_splits=[]
  remaining_data=data
  for i in range(n_split-1):
    split, remaining_data=train_test_split(remaining_data, test_size=1/n_split, stratify=remaining_data['Type of attack'])
    data_splits.append(split)
  data_splits.append(remaining_data)
  return data_splits

def analyze_splits(splits, original_data):
  for i, split in  enumerate(splits):
    st.write(f"Client{i+1} data shape:", split.shape)
    st.write(f"Client{i+1} data distribution:\n",split["Type of attack"].value_counts())

    # visualise class distribution
    fig,ax=plt.subplots()
    split["Type of attack"].value_counts().plot(kind='bar',ax=ax)
    ax.set_title(f'Client{i+1} class distribution')
    st.pyplot(fig)
  
    # statsistical summary
    st.write(f"Client{i+1} statistical summary")
    st.write(split.describe())
  
    #visualise feature distribution
    numerical_features=split.select_dtypes(include=['int64','float64']).columns
    for feature in numerical_features:
      fig, ax=plt.subplots()
      sns.histplot(split[feature],kde=True,ax=ax)
      ax.set_title(f'Client{i+1} {feature} distribution')
      st.pyplot(fig)
  
    # check for missing value
    st.write(f"Client {i+1} Missing Values")
    st.write(split.isnull().sum())

  # Provide download link for the split file
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
      split.to_excel(writer, index=False, sheet_name='Sheet1')
    st.download_button(
       label=f"Download Client {i+1} data as Excel",
       data=buffer.getvalue(),
       file_name=f"client_{i+1}_data.xlsx",
       mime="application/vnd.ms-excel")

# streamlit app

def main():
  st.title("ECU-IoHT data splitter and analyser")

  # FIle uploader
  upload_file=st.file_uploader("Upload your data file(Excel file)", type=["xlsx"])

  if upload_file is not None:
    data=load_data(upload_file)
    st.write("Data Shape:", data.shape)
    st.write("Class distribution:",data["Type of attack"].value_counts())

    n_split=st.number_input("Enter the number of splits:",min_value=2,max_value=10, value=3)

    if st.button("Perform stratified split"):
      splits= stratified_split(data,n_split)
      for i, split in enumerate(splits):
        split_file_path=f"client_{i+1}_data.xlsx"
        split.to_excel(split_file_path, index=False)
        st.write(f"Client{i+1} data saved to {split_file_path}")

      analyze_splits(splits, data)

if __name__=="__main__":
  main()
