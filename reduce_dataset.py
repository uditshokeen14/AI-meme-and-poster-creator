import pandas as pd

# Load cleaned dataset
df = pd.read_csv("cleaned_captions.csv")

# Randomly select 10000 captions
df_small = df.sample(n=10000, random_state=42)

# Save reduced dataset
df_small.to_csv("final_captions.csv", index=False)

print("Reduced dataset created!")
print("Total captions:", len(df_small))
