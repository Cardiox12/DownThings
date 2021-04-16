#!/usr/bin/python3

import requests
import sys
import re
import os
import zipfile
from pprint import pprint

id_regex = r"(:\d*)$"

# Algorithm
#   - Download links
#   - Decompress links

usage = """
    usage: down_things target_dir url [*urls]
"""

def print_status(identifier, message):
    print(f"[{identifier}] - {message}")

args = sys.argv[1:]

if len(args) < 2:
    print(usage)
else:
    target_dir = args[0]
    for url in args[1:]:
        if match := re.search(id_regex, url):
            thing_id = match.group(1)[1:]
            url = os.path.join(url, "zip")
            response = requests.get(url, allow_redirects=True)
            
            if response.status_code == 200:
                print_status(thing_id, "Download")
    
                filename = os.path.join(target_dir, f"thing_{thing_id}")
                filename_zip = f"{filename}.zip"
    
                with open(filename_zip, "wb") as f:
                    f.write(response.content)
                
                print_status(thing_id, f"Written {filename}")
    
                with zipfile.ZipFile(filename_zip, "r") as zip_file:
                    zip_file.extractall(filename)
    
                print_status(thing_id, f"Unzip {filename_zip}")

                os.remove(filename_zip)
            else:
                print_status(thing_id, "Download failed")
