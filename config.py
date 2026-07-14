import json
import os
import sys

class Config:
    def __init__(self):
        # Store in AppData/NasCloudMainServer/config.json
        self.path = "config.json"
        self.reload()

    def reload(self):
        if not os.path.exists(self.path):
            print(f"ERROR: Config file not found at {self.path}")
            print("Please configure the server properly before starting.")
            sys.exit(1)
            
        try:
            with open(self.path) as file:
                content = file.read().strip()
                if not content:
                    print(f"ERROR: Config file at {self.path} is empty.")
                    print("Please configure the server properly before starting.")
                    sys.exit(1)
                self.data = json.loads(content)
        except json.JSONDecodeError:
            print(f"ERROR: Config file at {self.path} is not valid JSON.")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR reading config: {e}")
            sys.exit(1)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)
        
config = Config()
