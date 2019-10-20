import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def import_photos(photo_export_filepath, output_path):

    base_path = Path(output_path)
    with Path(photo_export_filepath).open(encoding="UTF-8") as f:

        soup = BeautifulSoup(f.read(), "html.parser")
        items = soup.findAll("li", {"class": "active"})
        count = 0
        for item in items:
            a = item.findAll("a", {"class": "square-top"})[0]
            photo_id = a["data-id"]
            album_id = a["data-album-id"]
            label = a["aria-label"].replace("Preview photo ", "")
            print(label)
            div1 = item.findAll("div", {"class": "thumb-meta"})[0]
            upload_meta = div1.text
            save_location = base_path / album_id
            if not save_location.exists():
                save_location.mkdir()
            metafile = save_location / (photo_id + ".json")
            with metafile.open("w", encoding="UTF-8") as f:
                metadata = {
                    "photo_id": photo_id,
                    "album_id": album_id,
                    "label": label,
                    "upload_details": upload_meta
                }
                f.write(json.dumps(metadata, indent=2))
            # download the actual photo via the download link
            div2 = item.findAll("div", {"class": "action-bar-comment"})[0]
            a2 = div2.findAll("a")[0]
            url = a2["href"]
            download_to = save_location / (photo_id + ".jpg") # yes, we are assuming jpg
            resp = requests.get(url, headers={'Referer': 'https://groups.yahoo.com/'})
            with download_to.open("wb") as f:
                f.write(resp.content)
            count = count + 1
    print(count)

# Go to https://groups.yahoo.com/neo/groups/<your group name>/photos/photostream
# Then scroll down until all the photos have loaded (I know, this is totally impractical if you have a lot of photos)
# Then save the HTML file somewhere on your computer
# Then edit below line and uncomment and run the script
#import_photos("<downloaded HTML file>", "<export location>")

