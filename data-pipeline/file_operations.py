import os
import json

# Function to save content locally
def save_content_locally(contents, output_dir, search_term, batch_size=20):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(0, len(contents), batch_size):
        batch = contents[i:i + batch_size]
        json_file_name = os.path.join(output_dir, f"{search_term}-{i + 1}-{i + len(batch)}.json")
        with open(json_file_name, 'w', encoding='utf-8') as json_file:
            json.dump(batch, json_file, ensure_ascii=False, indent=4)
        print(f"Saved {json_file_name}")
