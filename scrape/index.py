import requests
from bs4 import BeautifulSoup

'''
{
    leagues: [
        {
            title: 'premier league',
            matches: [
                {
                    home_team: 'arsenal',
                    away_team: 'aston villa',
                    home_team_score: 2,
                    away_team_score: 1,
                    match_status: 'complete',
                    start_time: '2022-08-20T20:00:00Z',
                }
            ]
        }
    ]
}
'''


def scrape(url):
    leagues_class = 'qa-match-block'
    matches_class = 'gs-o-list-ui__item gs-u-pb-'
    team_class = 'gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc'
    home_team_score_class = 'sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft'
    away_team_score_class = 'sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft'

    leagues_to_scrape = ['premier league', 'spanish la liga',
                         'german bundesliga', 'italian serie a', 'french ligue 1']

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    leagues = soup.find_all('div', {'class': leagues_class})

    for league in leagues:
        league_name = league.find('h3').text

        if league_name.lower() not in leagues_to_scrape:
            continue

        scraped_matches = []

        matches = league.find_all('li', {'class': matches_class})

        for match in matches:
            home_team = match.find_all('span', {'class': team_class})[0].text
            away_team = match.find_all('span', {'class': team_class})[1].text
            home_team_score = None
            away_team_score = None
            match_status = None
            start_time = None

            if match.find('span', {'class': home_team_score_class + ' sp-c-fixture__number--live-sport'}):
                home_team_score = match.find(
                    'span', {'class': home_team_score_class + ' sp-c-fixture__number--live-sport'}).text
                away_team_score = match.find(
                    'span', {'class': away_team_score_class + ' sp-c-fixture__number--live-sport'}).text
                match_status = 'playing'
            elif match.find('span', {'class': 'sp-c-fixture__number sp-c-fixture__number--time'}):
                home_team_score = None
                away_team_score = None
                match_status = 'not_started'
                start_time = match.find(
                    'span', {'class': 'sp-c-fixture__number sp-c-fixture__number--time'}).text
            else:
                home_team_score = match.find(
                    'span', {'class': home_team_score_class}).text
                away_team_score = match.find(
                    'span', {'class': away_team_score_class}).text
                match_status = 'finished'

            scraped_matches.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_team_score': home_team_score or None,
                'away_team_score': away_team_score or None,
                'match_status': match_status,
                'start_time': start_time or None
            })

        data.append({
            'title': league_name,
            'matches': scraped_matches
        })

    return data
