import re
import os

def extract_and_write_dialogue():
    script_path = os.path.join('game', 'script.rpy')
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except FileNotFoundError:
        print(f"Error: {script_path} not found.")
        return

    lines = script_content.splitlines()

    dialogues = {
        "skr": [], # Fujiwara Sakura
        "akn": [], # Kazami Akane
        "aoi": [], # Kobayakawa Aoi
        "ao": []   # Kirishima Ao
    }

    # Regex to capture dialogue, handling comments and Ren'Py text tags
    dialogue_pattern = re.compile(r'^\s*(skr|akn|aoi|ao)\s*"(.*?)"(?:\s*#.*)?$')

    for line in lines:
        match = dialogue_pattern.match(line)
        if match:
            char_id = match.group(1)
            dialogue_text = match.group(2)
            
            # Clean up Ren'Py text tags like {fast}, {nw}, etc.
            cleaned_text = re.sub(r'{.*?}', '', dialogue_text)
            
            dialogues[char_id].append(cleaned_text)

    # Mapping from character ID to filename
    output_files = {
        "skr": "sakura_lines.txt",
        "akn": "akane_lines.txt",
        "aoi": "aoi_lines.txt",
        "ao": "ao_lines.txt"
    }

    for char_id, filename in output_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            for line in dialogues[char_id]:
                f.write(line + '\n')
        print(f"Created {filename} with {len(dialogues[char_id])} lines.")

if __name__ == "__main__":
    extract_and_write_dialogue()