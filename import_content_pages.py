import os
from pathlib import Path
from functools import partial
import requests

API_URL = "http://local.music-scene-data.com:8000"


# make pages
content_dir = None


content_dir = Path(os.path.dirname(__file__), "content")

# TODO maybe use json for front matter format?

def write_venue(path, obj):

    print(f"Writing {path}")
    file = open(path, "w")
    _ = partial(print, **{'file': file})

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
    _("---")
    if obj['description']:
        _(obj["description"])


def main():

    # Venues
    venues = requests.get(f"{API_URL}/venue/").json()
    for venue in venues:
        filename = venue["slug"]
        path = Path(content_dir, "events/venue", f"{filename}.md")
        # if not path.is_file():
        write_venue(path, venue)


if __name__ == "__main__":
    main()
