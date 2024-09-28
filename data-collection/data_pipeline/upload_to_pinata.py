import os
import requests
import json

# Function to upload JSON files to Pinata
def upload_to_pinata(directory, pinata_jwt):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {'Authorization': f"Bearer {pinata_jwt}"}

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file_path = os.path.join(directory, filename)
            with open(json_file_path, 'rb') as file:
                files = {'file': (filename, file)}  # Include the filename in the tuple
                
                # Optional: Prepare metadata
                metadata = {
                    "name": filename,
                    "keyvalues": {
                        "customKey": "customValue"  # Optional custom metadata
                    }
                }
                
                # Sending the request
                response = requests.post(url, headers=headers, files=files, data={"pinataMetadata": json.dumps(metadata)})

                if response.status_code == 200:
                    print(f"File {filename} uploaded successfully:", response.json())
                else:
                    print(f"Failed to upload {filename}: {response.status_code}, {response.text}")

# Example usage:
# Make sure to provide the correct directory path and your Pinata JWT
# upload_to_pinata('./usdac_data_scrap', 'your_pinata_jwt_here')
