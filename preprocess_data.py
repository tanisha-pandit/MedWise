import pandas as pd
import json
import itertools

# Load dataset
file_path = "./FinalMedicineDataset.csv"
data = pd.read_csv(file_path)

# Preprocess dataset
processed_data = []
for _, row in data.iterrows():
    medicine_name = row['Medicine Name']
    composition = row.get('composition', 'Information not available')
    uses = row.get('uses', 'Information not available')
    side_effects = row.get('side effects', 'Information not available')
    substitutes = row.get('substitutes', 'Information not available')
    
    # Single-intent examples
    processed_data.append({
        "instruction": f"What is the composition of {medicine_name}?",
        "response": f"Composition: {composition}"
    })
    processed_data.append({
        "instruction": f"What are the uses of {medicine_name}?",
        "response": f"Uses: {uses}"
    })
    processed_data.append({
        "instruction": f"What are the side effects of {medicine_name}?",
        "response": f"Side Effects: {side_effects}"
    })
    processed_data.append({
        "instruction": f"What are the substitutes for {medicine_name}?",
        "response": f"Substitutes: {substitutes}"
    })
    
    # Multi-intent examples with all combinations of intents
    fields = ['composition', 'uses', 'side effects', 'substitutes']
    values = [composition, uses, side_effects, substitutes]

    # Generate all combinations of the fields
    for r in range(2, len(fields) + 1):  # Combinations of at least 2 fields
        for combination in itertools.combinations(range(len(fields)), r):
            instruction_parts = [fields[i] for i in combination]
            response_parts = [values[i] for i in combination]
            
            instruction = f"What are the " + " and ".join(instruction_parts) + f" of {medicine_name}?"
            response = "\n".join([f"{field.capitalize()}: {value}" for field, value in zip(instruction_parts, response_parts)])
            
            processed_data.append({
                "instruction": instruction,
                "response": response
            })
    
    # Additional multi-intent example with all fields
    instruction = f"Give me the details of {medicine_name}."
    response = f"Composition: {composition}\nUses: {uses}\nSide Effects: {side_effects}\nSubstitutes: {substitutes}"
    processed_data.append({
        "instruction": instruction,
        "response": response
    })

# Save processed data
output_path = "./processed_medicine_data.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(processed_data, f, indent=4, ensure_ascii=False)

print(f"Processed data saved to {output_path}")
