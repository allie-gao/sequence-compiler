import requests
import pandas as pd

SERVICE_URL = 'https://rest.kegg.jp/get/'

TIMEOUT_SECONDS = 15

# Loading the csv file into a pandas DataFrame
dataframe = pd.read_csv('regscore_0.csv')

# Create a session for writing data to a text file
f = open('kegg_regulators.txt', 'w')

# Iterating through each row in the DataFrame
for index, row in dataframe.iterrows():
    # Getting the organism code and regulator from the current row
    organism_code = row['Organism_code'].lower()
    regulator = row['Regulator']

    # Preparing the URL
    url = f"{SERVICE_URL}{organism_code}:{regulator}/aaseq"

    # Making the request
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        # Saving the response content to a text file
        f.write(response.text + "\n\n")  # Adding two new lines at the end of the file

        print(f"Successfully saved data for {organism_code}:{regulator}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {organism_code}:{regulator}: {e}")

# Closing the file after writing all data
f.close()

