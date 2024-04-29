import sys
import os
import re
import requests
import bs4
from tqdm import tqdm
from pathlib import Path


def download_twitter_video(url, shortcode):
    api_url = f"https://twitsave.com/info?url={url}"
    response = requests.get(api_url)
    data = bs4.BeautifulSoup(response.text, "html.parser")
    download_button = data.find_all("div", class_="origin-top-right")[0]
    quality_buttons = download_button.find_all("a")
    highest_quality_url = quality_buttons[0].get("href")  # Highest quality video url

    file_name = re.sub(r"[^a-zA-Z0-9]+", ' ', shortcode).strip() + ".mp4"  # Remove special characters from file name
    download_path = os.path.join('Media', 'Twitter', file_name)

    response = requests.get(highest_quality_url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open(download_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    return download_path
