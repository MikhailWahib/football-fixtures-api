# Football Fixtures API

## Description

This API provides access to the Top-5-leagues football fixtures.
The data is scraped from [BBC Sport](https://www.bbc.com/sport/football/scores-fixtures) using [Python](https://www.python.org/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

The API uses Redis for caching results, It caches todays results for 30 seconds and the rest for 30 days.

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://requests.readthedocs.io/en/latest/)

## Usage

### Endpoints

- [GET] `/today`
- [GET] `/{date}` - date format: YYYY-MM-DD

### Response example:

```json
{
  "leagues": [
    {
      "title": "Premier League",
      "matches": [
        {
          "home_team": "Manchester United",
          "away_team": "Manchester United",
          "match_status": "finished | playing | upcoming",
          "home_team_score": "3",
          "away_team_score": "0"
        }
      ]
    }
  ]
}
```

## Local Development

### Clone repository

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

1- Run Redis on default port 6379

2- Run the API with
```bash
flask run
```
