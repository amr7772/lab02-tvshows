# TV Shows Summary

This program downloads a list of TV shows from TVmaze and summarizes it: how many shows are in each genre, the average rating for each language, and how many shows premiered in each decade. It gives a quick picture of what the catalogue looks like.

## Data source

https://api.tvmaze.com/shows?page=0

Each record is one TV show, with its name, language, genres, rating, premiere date and network. This page returns 240 shows.

## Setup

    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Run

    python records.py

## Example output

```json
"shows_per_decade": {
  "2010s": 179,
  "2000s": 51,
  "1990s": 8,
  "1980s": 2
}
```

Almost all the shows on this page premiered in the 2000s and 2010s. Drama is the most common genre by far (154 shows).

## Data quirks

- **A show can have several genres, or none.** So I loop over the genres inside the loop over the shows. Shows with an empty genre list are not counted in any genre (5 shows on this page).
- **Some shows have no rating.** Their rating is `null`. I skip them when calculating the average so they don't pull it down as zeros (4 shows).
- **Some shows have no network.** It is `null` for streaming shows (11 shows). I count these in `missing_values`.
- The premiere date is a text like `"2013-06-24"`, so I take the first three characters and add `"0s"` to get the decade.

## Design choices

- **list**: the shows come from the API as a list, and I also collect the ratings of each language in a list before averaging them.
- **dict**: every count (genre, decade, language) maps a name to a number, and the final summary is a dict because it goes straight into JSON.
- **set**: to count how many different genres exist. A set keeps each genre only once.

## Known limitations

- It only reads the first page (240 shows), not the whole TVmaze catalogue.
- With more time I would read more pages and add tests with a few hand-made shows.
