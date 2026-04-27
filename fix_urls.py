import re
import os

file_path = 'guest_landing_page/code.html'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('http://localhost:5001', 'http://127.0.0.1:5001')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

details_path = 'guest_landing_page/room_details.html'
if os.path.exists(details_path):
    with open(details_path, 'r', encoding='utf-8') as f:
        d_content = f.read()
    d_content = d_content.replace('http://localhost:5001', 'http://127.0.0.1:5001')
    with open(details_path, 'w', encoding='utf-8') as f:
        f.write(d_content)

# Also update the login page
login_path = 'auth/login.html'
if os.path.exists(login_path):
    with open(login_path, 'r', encoding='utf-8') as f:
        l_content = f.read()
    l_content = l_content.replace('http://localhost:5001', 'http://127.0.0.1:5001')
    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(l_content)

print("Updated localhost to 127.0.0.1 in all frontend files.")
