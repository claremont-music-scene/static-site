import os
from pathlib import Path
from functools import partial
from urllib.parse import urlparse

import requests

API_URL = "http://local.music-scene-data.com:8000"


content_dir = Path(os.path.dirname(__file__), "content")


def write_venue(path, obj, is_bundle=False):

    # TODO create new bundle dir if needed
    if is_bundle:
        if not path.parent.exists():
            path.mkdir(path.parent)
        print(f"Writing Bundle {path}")
    else:
        print(f"Writing {path}")

    file = open(path, "w")
    _ = partial(print, **{"file": file})

    _("---")
    _(f"title: {obj['name']}")
    _("type: venue")
    _(f"date: {obj['date_modified']}")
    _("draft: false")
    _("layout: venue-single")
    for field in [
        "website",
        "calendar_url",
        "facebook",
        "twitter",
        "instagram",
        "phone",
        "email",
        "address_street",
        "address_city",
        "address_full",
    ]:
        if obj[field]:
            _(f"{field}: {obj[field]}")

    # handle images
    # download file and place in dir if not exist
    if obj["image"]:
        response = requests.get(obj["image"])
        if response.status_code == 200:
            img_dir = os.path.dirname(path)
            img_fname = os.path.basename(urlparse(obj["image"]).path)
            img_path = Path(img_dir, img_fname)

            # TODO check if file exists at destination
            with open(img_path, "wb") as f:
                print(f"\tWriting {img_path}")
                f.write(response.content)

            _(f"primary_image: {img_fname}")
    # write primary-image field
    _("---")
    if obj["description"]:
        _(obj["description"])


def main():

    # Venues
    venues = requests.get(f"{API_URL}/venues/").json()
    for venue in venues:
        filename = venue["slug"]

        if venue["image"]:
            path = Path(content_dir, f"events/venues/{filename}/index.md")
            # overwrites
            write_venue(path, venue, is_bundle=True)
        else:
            path = Path(content_dir, f"events/venues/{filename}.md")
            # overwrites
            write_venue(path, venue)


if __name__ == "__main__":
    main()
