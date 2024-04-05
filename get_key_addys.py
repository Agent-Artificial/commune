from pathlib import Path
import json
from loguru import logger

filepath = "~/.commune/key"

file_path = Path(filepath).expanduser().resolve()

files = file_path.iterdir()

adresses = []
for file in files:
    try:
        data = json.loads(file.read_text())["data"]
        adresses.append(f"{json.loads(data)['ss58_address']}")
        adresses.append(f"{json.loads(data)['path']}")
    except:
        logger.warning(f"Failed to load file: {file}")

print("\n".join(adresses))



