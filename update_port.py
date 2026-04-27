import os

files = [
    'guest_landing_page/code.html',
    'guest_landing_page/room_details.html',
    'auth/login.html'
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(':5001', ':5005')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path} to use port 5005")
