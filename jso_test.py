import json

def get_config():
    try:
        with open("shared_config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def process_data():
    config = get_config()
    if not config:
        print("No configuration found")
        return
    
    # Example usage
    for column, settings in config.items():
        print(f"Processing column: {column}")
        print(f"Type: {settings['type']}")
        
        if settings['type'] == 'phone':
            print(f"Country code: {settings.get('phone_code', '')}")
        
        if 'unit' in settings:
            print(f"Measurement unit: {settings['unit']}")

if __name__ == "__main__":
    process_data()