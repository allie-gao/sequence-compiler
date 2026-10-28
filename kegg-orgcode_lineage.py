import requests
import pandas as pd

# Loading the website table and regulator data into pandas DataFrames
dataframe_web = pd.read_html("br08606.html")[1]
dataframe_regulators = pd.read_csv('regscore_0.csv')

# Iterating through each row in the regulator DataFrame
matched_dataframes = []
for index, row in dataframe_regulators.iterrows():
    try:
        # Getting the organism code and regulator from the current row
        organism_code = row['Organism_code'].lower()

        # Finding any rows in the Organisms column that have the code
        matched_row = dataframe_web.loc[dataframe_web["Organisms"] == organism_code]

        # Making sure it found something, if so, save it to the list
        if not matched_row.empty:
            matched_dataframes.append(matched_row)
            print("Matched row found for organism code:", organism_code)
        else:
            print(f"No data found for {organism_code}")

    except Exception as e:
        print(f"Error fetching data: {e}")

# Concatenating all matched DataFrames into a single DataFrame, saving the results
if matched_dataframes:
    final_dataframe = pd.concat(matched_dataframes)

    # Filtering out the columns that we want to keep
    final_dataframe = final_dataframe[['Category.1', 'Category.2', "Organisms","Organisms.2"]]  # Adjust column names as necessary

    # Saving the final DataFrame to a CSV file
    final_dataframe.to_csv('kegg_lineages.csv', index=False)
    print("Successfully saved matched organisms to 'kegg_lineages.csv'")
else:
    print("No matched organisms found.")
    exit(1)
