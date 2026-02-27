import pandas as pd

# Load dataset
df = pd.read_csv("imgflip_dataset.csv")

# Use correct caption column
df['full_caption'] = df['CaptionText'].fillna('').astype(str)

# Remove empty captions
df = df[df['full_caption'].str.strip() != ""]

# Remove duplicates
df = df.drop_duplicates(subset=['full_caption'])

# Remove very long captions (keep meme style)
df = df[df['full_caption'].str.len() < 120]

# Remove captions with only numbers or symbols
df = df[df['full_caption'].str.contains('[a-zA-Z]', regex=True)]

# Add event placeholder
df['caption_template'] = "{event} – " + df['full_caption']

# Keep only required column
cleaned_df = df[['caption_template']]

# Save cleaned dataset
cleaned_df.to_csv("cleaned_captions.csv", index=False)

print("✅ Dataset cleaned successfully!")
print("Total usable captions:", len(cleaned_df))
