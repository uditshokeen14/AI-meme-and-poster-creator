import pandas as pd

# Load TSV file
df = pd.read_csv("memes_data.tsv", sep="\t")

# Save as CSV
df.to_csv("imgflip_dataset.csv", index=False)

print("Conversion complete!")
