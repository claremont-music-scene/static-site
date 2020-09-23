import os
from pathlib import Path
from functools import partial
from urllib.parse import urlparse

import requests

API_URL = "http://local.music-scene-data.com:8000/api"


content_dir = Path(os.path.dirname(__file__), "content")


def write_venue(path, obj, is_bundle=False):

    # TODO check if leaf is being replaced by bundle and remove the leaf file

    if is_bundle:
        if not path.parent.exists():
            os.mkdir(path.parent)
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


def write_post(path, obj, is_bundle=False):

    # TODO check if leaf is being replaced by bundle and remove the leaf file

    if is_bundle:
        if not path.parent.exists():
            os.mkdir(path.parent)
        print(f"Writing Bundle {path}")
    else:
        print(f"Writing {path}")

    file = open(path, "w")
    _ = partial(print, **{"file": file})

    _("---")
    _(f"title: {obj['title']}")
    _("type: news")
    _(f"date: {obj['date_modified']}")
    _("draft: false")
    for field in [
            "slug",
            "teaser",
            #"author",
            "date_published"
    ]:
        if obj[field]:
            _(f"{field}: {obj[field]}")

    _(f"author: {obj['author']['first_name']} {obj['author']['last_name']}")

    # handle images
    # download file and place in dir if not exist
    # TODO refactor as handle_image
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

    # End Front Matter
    _("---")

    # Content section
    if obj["body"]:
        _(obj["body"])

def import_venues():
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

def import_news():
    # News
    news = requests.get(f"{API_URL}/posts/").json()
    for post in news:
        filename = post["slug"]

        if post["image"]:
            path = Path(content_dir, f"news/{filename}/index.md")
            # overwrites
            write_post(path, post, is_bundle=True)
        else:
            path = Path(content_dir, f"news/{filename}.md")
            # overwrites
            write_post(path, post)


def main():
    import_venues()
    import_news()



if __name__ == "__main__":
    main()
