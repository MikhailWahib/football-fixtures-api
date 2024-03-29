import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from lib.cache_data import cache_data

'''
data: [
    {
        title: 'premier league',
        matches: [
            {
                home_team: 'arsenal',
                away_team: 'aston villa',
                home_team_score: 2,
                away_team_score: 1,
                match_status: 'complete',
                start_time: '14:00',
            }
        ]
    }
]
'''


def scrape(url='/'):
    BASE_URL = 'https://www.bbc.com/sport/football/scores-fixtures'
    data_date_string = url.split('/')[-1]

    leagues_class = 'qa-match-block'
    matches_class = 'gs-o-list-ui__item gs-u-pb-'
    team_class = 'gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc'
    home_team_score_class = 'sp-c-fixture__number sp-c-fixture__number--home'
    away_team_score_class = 'sp-c-fixture__number sp-c-fixture__number--away'
    live_score_class = 'sp-c-fixture__number--live-sport'
    finished_score_class = 'sp-c-fixture__number--ft'
    not_started_date_class = 'sp-c-fixture__number sp-c-fixture__number--time'

    leagues_to_scrape = ['premier league', 'spanish la liga',
                         'german bundesliga', 'italian serie a', 'french ligue 1', 'champions league']

    try:
        response = requests.get(f"{BASE_URL}{url}")
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        data = []

        leagues = soup.find_all('div', {'class': leagues_class})

        if not leagues:
            return []

        for league in leagues:
            league_name = league.find('h3').text

            if league_name.lower() not in leagues_to_scrape:
                continue

            scraped_matches = []

            matches = league.find_all('li', {'class': matches_class})

            for match in matches:
                home_team = match.find_all(
                    'span', {'class': team_class})[0].text
                away_team = match.find_all(
                    'span', {'class': team_class})[1].text
                home_team_score = None
                away_team_score = None
                match_status = None
                start_time = None

                # check if match is live
                if match.find('span', {'class': f"{home_team_score_class} {live_score_class}"}):
                    home_team_score = match.find(
                        'span', {'class': f"{home_team_score_class} {live_score_class}"}).text
                    away_team_score = match.find(
                        'span', {'class': f"{away_team_score_class} {live_score_class}"}).text
                    match_status = 'playing'

                # check if match is not started
                elif match.find('span', {'class': not_started_date_class}):
                    home_team_score = None
                    away_team_score = None
                    match_status = 'not_started'
                    start_time = match.find(
                        'span', {'class': not_started_date_class}).text

                # check if match is finished
                elif match.find('span', {'class': f"{home_team_score_class} {finished_score_class}"}):
                    home_team_score = match.find(
                        'span', {'class': f"{home_team_score_class} {finished_score_class}"}).text
                    away_team_score = match.find(
                        'span', {'class': f"{away_team_score_class} {finished_score_class}"}).text
                    match_status = 'finished'

                scraped_matches.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'match_status': match_status,
                })

                # add scores if match is finished or playing
                if home_team_score is not None:
                    scraped_matches[-1]['home_team_score'] = home_team_score
                    scraped_matches[-1]['away_team_score'] = away_team_score

                # add start time if match is not started
                if start_time is not None:
                    scraped_matches[-1]['start_time'] = start_time

            data.append({
                'title': league_name,
                'matches': scraped_matches
            })
            # cache data if date is not today
            if url != '/':
                cache_data(data, data_date_string)

        return data

    except Exception as e:
        print('Something went wrong while scraping the data: ', e)
        return None
