# Di Termux/Linux
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests urllib3 concurrent.futures

# Download tools
curl -O https://raw.githubusercontent.com/volox/terminator/main/volox_terminator_v5.py

# Jalankan
python volox_terminator_v5.py