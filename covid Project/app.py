from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV
df = pd.read_csv("covid_vaccine_statewise.csv")

# Remove spaces from column names
df.columns = df.columns.str.strip()

print("COLUMNS =", df.columns.tolist())
print("ROWS =", len(df))

# Detect state column
state_col = "State"

# Find first dose column automatically
first_col = None
second_col = None
male_col = None
female_col = None

for col in df.columns:
    low = col.lower()

    if "first" in low and ("dose" in low or "administered" in low):
        first_col = col

    if "second" in low and ("dose" in low or "administered" in low):
        second_col = col

    if "male" in low and "doses" in low:
        male_col = col

    if "female" in low and "doses" in low:
        female_col = col

# Clean
df = df.dropna(subset=[first_col, second_col])  # Drop rows where doses are NaN
df = df.fillna(0)

# Latest row per state
latest = df.groupby(state_col, as_index=False).last()

records = latest[[state_col, first_col, second_col]].to_dict(orient="records")

first = int(latest[first_col].sum())
second = int(latest[second_col].sum())
male = int(latest[male_col].sum()) if male_col else 0
female = int(latest[female_col].sum()) if female_col else 0

@app.route("/")
def home():
    return render_template(
        "index.html",
        first=first,
        second=second,
        male=male,
        female=female,
        records=records,
        state_col=state_col,
        first_col=first_col,
        second_col=second_col
    )

app.run(debug=True)