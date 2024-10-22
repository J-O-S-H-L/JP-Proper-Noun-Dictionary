import re
import json

# Sample text lines with varying numbers of readings
with open("Proper Nouns.txt", "r", encoding="utf-8") as f:
    text_data = f.read()

# Split the text into lines
lines = text_data.strip().split("\n")


# Function to process each line
def process_line(line):
    # Split the line into its components (term, readings, id)
    parts = line.split("\t")

    # Check if the line has at least 3 parts
    if len(parts) < 3:
        print(f"Skipping malformed line: {line}")
        return None

    term = parts[0]
    readings = parts[1]
    term_id = int(parts[2])

    # Use regex to extract readings and their percentages
    matches = re.findall(r"\((.*?)\)([^\(]+)\((\d+)%\)", readings)

    if not matches:
        print(f"No valid readings found for: {line}")
        return None

    # Sort readings by percentage in descending order
    sorted_readings = sorted(matches, key=lambda x: int(x[2]), reverse=True)

    # Extract the tag of the first (highest percentage) reading
    primary_tag = sorted_readings[0][0]

    # Prepare definitions (readings with percentages)
    definitions = [
        f"{reading[1]} ({reading[2]}%) - {reading[0]}" for reading in sorted_readings
    ]

    # Construct the JSON-like structure, replacing the first "n" with the primary tag
    output_entry = [
        term,
        sorted_readings[0][1],
        primary_tag,
        "n-pr",
        0,
        definitions,
        term_id,
        "n-pr",
    ]

    return output_entry


# Process each line, skipping None results from invalid lines
output_data = [entry for entry in (process_line(line) for line in lines) if entry]

# Convert to JSON and write to file (or just print)
json_output = json.dumps(output_data, ensure_ascii=False, indent=4)

# Optionally write to a file
with open("dict/term_bank_1.json", "w", encoding="utf-8") as f:
    f.write(json_output)
