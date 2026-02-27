import pandas as pd
import random

# Load dataset once
df = pd.read_csv("final_captions.csv")
templates = df["caption_template"].tolist()

def generate_captions(event_name):
    selected = random.sample(templates, 3)
    return [caption.format(event=event_name) for caption in selected]