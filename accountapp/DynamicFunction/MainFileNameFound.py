from urllib.parse import urlparse
import os

def get_file_name_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract the path and get the base name
    file_name = os.path.basename(parsed_url.path)
    return file_name
