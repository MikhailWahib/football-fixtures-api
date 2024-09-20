import requests
from bs4 import BeautifulSoup
from .cache_data import cache_data

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
    print("Scaping.........")
    BASE_URL = 'https://www.bbc.com/sport/football/scores-fixtures'
    data_date_string = url.split('/')[-1]

    leagues_class = 'ssrcss-1jkg1a7-HeaderWrapper e4zdov50' #div
    matches_class = 'ssrcss-1bjtunb-GridContainer e1efi6g55' #div
    team_name_class = 'ssrcss-1p14tic-DesktopValue emlpoi30' #span
    home_team_score_class = 'ssrcss-qsbptj-HomeScore e56kr2l2' #div
    away_team_score_class = 'ssrcss-fri5a2-AwayScore e56kr2l1' #div
    ft_div_class = 'ssrcss-1uqnn64-StyledPeriod e307mhr0' #div
    time_div_class = 'ssrcss-etkxi3-StyledCentre ejsemf30' #div

    leagues_to_scrape = ['premier league', 'spanish la liga',
                         'german bundesliga', 'italian serie a', 'french ligue 1', 'champions league', 'internationals', 'uefa euro 2024']

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
            league_name = league.find('h2')
            if league_name:
                league_name = league.find('h2').text
            else:
                league_name = ''

            if league_name.lower() not in leagues_to_scrape:
                continue

            scraped_matches = []

            matches = league.find_all('div', {'class': matches_class})

            for match in matches:
                home_team = match.find_all(
                    'span', {'class': team_name_class})[0].text
                away_team = match.find_all(
                    'span', {'class': team_name_class})[1].text
                home_team_score = None
                away_team_score = None
                match_status = None
                start_time = None

                # check if match is not started
                # if the time element exisits, that means that the match hasn't started yet
                if match.find('div', {'class': time_div_class}):
                    home_team_score = None
                    away_team_score = None
                    match_status = 'not_started'
                    start_time = match.find(
                        'div', {'class': time_div_class}).text

                # check if match is finished
                # if the match div has the FT div, that means that the match has ended.
                elif match.find('div', {'class': {ft_div_class}}):
                    home_team_score = match.find(
                        'div', {'class': {home_team_score_class}}).text
                    away_team_score = match.find(
                        'div', {'class': {away_team_score_class}}).text
                    match_status = 'finished'

                # Match is live
                else:
                    match_status = 'playing'


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
                    scraped_matches[-1]['start_time'] = start_time[:5]

            data.append({
                'title': league_name,
                'matches': scraped_matches
            })
            # cache data
            cache_data(data, data_date_string or 'today')

        return data

    except Exception as e:
        print('Something went wrong while scraping the data: ', e)
        return None
