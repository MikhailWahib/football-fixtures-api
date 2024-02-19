# Football Fixtures API

## Description

This API provides access to the Top-5-leagues football fixtures for the past and future 2 weeks.
The data is scraped from [BBC Sport](https://www.bbc.com/sport/football/scores-fixtures) using [Python](https://www.python.org/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

The API uses Redis for caching past and future fixtures.

## Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [requests](https://requests.readthedocs.io/en/latest/)

## Usage

### Endpoints

- [GET] `/today`
- [GET] `/{date}` - date format: YYYY-MM-DD

## Local Development

### Clone repository

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
flask run
```
