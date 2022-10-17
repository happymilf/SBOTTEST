from pathlib import Path
import json

def get_data(field : str) -> str:
    p = Path(__file__).with_name('bot_text.json')
    config = open(p)
    output = config.read()
    output = json.loads(output)
    return output[field]

def change_data(field : str, text : str) -> None:
    p = Path(__file__).with_name('bot_text.json')
    config = open(p)
    output = config.read()
    output = json.loads(output)
    output[field] = text
    with open(p, 'w') as f:
        json.dump(output, f)