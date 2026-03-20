import pandas as pd

data = pd.read_csv("../data/students.csv")

# Check missing values
print(data.isnull().sum())

# Remove duplicates
data = data.drop_duplicates()

# Save cleaned dataset
data.to_csv("../data/cleaned_students.csv", index=False)

#print("Data cleaned and saved.")
