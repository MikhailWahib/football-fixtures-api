# Football Scores API

## Description

This API provides data about upcoming and finished football matches.
The data is scraped from [BBC Sport](https://www.bbc.com/sport/football/scores-fixtures) using [Python](https://www.python.org/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

The API uses Redis for caching results, It caches todays results for 30 seconds and the rest for 30 days.

The API is documented using [Swagger UI](https://github.com/swagger-api/swagger-ui).

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Swagger UI](https://github.com/swagger-api/swagger-ui)
## Usage

### Endpoints

- [GET] `/today`
  - Optional query parameter: `league` - supported values: `pl`, `sl`, `gl`, `sa`, `fl`, `cl`, `in`
- [GET] `/{date}` - date format: YYYY-MM-DD
  - Optional query parameter: `league` - supported values: `pl`, `sl`, `gl`, `sa`, `fl`, `cl`, `in`

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
          "match_status": "finished | playing | not started",
          "home_team_score": "3",
          "away_team_score": "0",
          // or
          "start_time": "15:00"
        }
      ]
    }
  ]
}
```

## Documentation

### Open Swagger UI

- Run your server and visit `http://localhost:5000/docs` in your browser.

## Local Development

### Clone repository

```bash
git clone https://github.com/MikhailWahib/football-scores-api.git
```

### Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

- Install (if not) and run Redis server on default port **6379**. **(mandatory)**

```bash
redis-server
```

- Run the API with
```bash
flask run
```
