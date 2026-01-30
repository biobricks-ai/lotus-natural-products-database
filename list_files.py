import requests

def list_files():
    record_id = "7534071"
    url = f"https://zenodo.org/api/records/{record_id}"
    response = requests.get(url)
    data = response.json()
    for f in data['files']:
        print(f['key'], f['size'])

if __name__ == "__main__":
    list_files()
