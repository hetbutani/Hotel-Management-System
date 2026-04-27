import os

files = ['index.html', 'room_details.html']

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Update internal links
        content = content.replace('guest_landing_page/room_details.html', 'room_details.html')
        content = content.replace('guest_landing_page/code.html', 'index.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated links in {file_path}")
