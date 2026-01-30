import requests
import os
import sys

def download_data():
    record_id = "7534071"
    url = f"https://zenodo.org/api/records/{record_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # We want the metadata file as it is larger and likely contains the structures
    target_filename = "230106_frozen_metadata.csv.gz"
    target_file = None
    
    for f in data['files']:
        if f['key'] == target_filename:
             target_file = f
             break
    
    if not target_file:
         # Fallback
         print("Specific metadata file not found, looking for largest csv.gz")
         files = sorted(data['files'], key=lambda x: x['size'], reverse=True)
         for f in files:
             if f['key'].endswith('.csv.gz'):
                 target_file = f
                 break

    if not target_file:
        print("No suitable file found.")
        sys.exit(1)

    print(f"Downloading {target_file['key']}...")
    download_url = target_file['links']['self']
    
    # Download
    os.makedirs('download', exist_ok=True)
    local_path = os.path.join('download', target_file['key'])
    
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"Downloaded to {local_path}")

if __name__ == "__main__":
    download_data()
