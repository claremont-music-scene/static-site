import os
from pathlib import Path

import requests

API_URL = "http://local.music-scene-data.com:8000"


# make pages
content_dir = None


content_dir = Path(os.path.dirname(__file__), "content")


def write_venue(path, obj):
    # title, date, draft
    print(f"Writing {path}")

    file = open(path, "w")
    print("---", file=file)

    print(f"title: {obj['name']}", file=file)
    print(f"date: {obj['date_modified']}", file=file)
    print("draft: false", file=file)
    print("layout: venue-single", file=file)

    for field in ['twitter', 'facebook', 'website', 'address_street']:
        if obj[field]:
            print(f"{field}: {obj[field]}", file=file)

    print("---\n", file=file)
    if obj['description']:
        print(obj["description"], file=file)


def main():

    # Venues
    venues = requests.get(f"{API_URL}/venues/").json()
    for venue in venues:
        filename = venue["slug"]
        path = Path(content_dir, "events/venues", f"{filename}.md")
        # if not path.is_file():
        write_venue(path, venue)


if __name__ == "__main__":
    main()
