# records.py
import json
import sys
from pathlib import Path

import requests

SOURCE_URL = "https://api.tvmaze.com/shows?page=0"
OUTPUT = Path("summary.json")


def fetch_shows(url):
    """Download the list of shows and return it as Python objects."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def count_shows_per_genre(shows):
    """Count how many shows belong to each genre."""
    counts = {}
    for show in shows:
        for genre in show.get("genres", []):  # a show can have many genres, or none
            counts[genre] = counts.get(genre, 0) + 1
    return counts


def average_rating_by_language(shows):
    """Return the average rating for each language, skipping shows with no rating."""
    ratings = {}
    for show in shows:
        rating = (show.get("rating") or {}).get("average")
        language = show.get("language")
        if rating is None or language is None:
            continue
        ratings.setdefault(language, []).append(rating)

    return {lang: round(sum(values) / len(values), 2) for lang, values in ratings.items()}


def count_shows_per_decade(shows):
    """Count how many shows premiered in each decade."""
    counts = {}
    for show in shows:
        premiered = show.get("premiered")  # looks like "2013-06-24"
        if not premiered:
            continue
        decade = premiered[:3] + "0s"
        counts[decade] = counts.get(decade, 0) + 1
    return counts


def count_missing_values(shows):
    """Count the shows with no genre, no rating or no network."""
    return {
        "no_genre": len([s for s in shows if not s.get("genres")]),
        "no_rating": len([s for s in shows if (s.get("rating") or {}).get("average") is None]),
        "no_network": len([s for s in shows if s.get("network") is None]),
    }


def build_summary(shows):
    """Combine the aggregations into one dict ready to write."""
    all_genres = {genre for show in shows for genre in show.get("genres", [])}
    return {
        "source_url": SOURCE_URL,
        "records_processed": len(shows),
        "number_of_genres": len(all_genres),
        "shows_per_genre": count_shows_per_genre(shows),
        "average_rating_by_language": average_rating_by_language(shows),
        "shows_per_decade": count_shows_per_decade(shows),
        "missing_values": count_missing_values(shows),
    }


def write_summary(summary, path):
    """Write the summary to a JSON file."""
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main():
    """Download the shows, summarize them and save the result."""
    try:
        shows = fetch_shows(SOURCE_URL)
    except requests.exceptions.RequestException as error:
        print("Could not download the data. Check your internet connection.")
        print("Details:", error)
        sys.exit(1)

    summary = build_summary(shows)
    write_summary(summary, OUTPUT)
    print(f"Done: {len(shows)} shows processed. Summary saved to {OUTPUT}")


if __name__ == "__main__":
    main()
