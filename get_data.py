import requests
import urllib3
from session import session

urllib3.disable_warnings()

def get_data(year=2023, day=1):
    urllib3.disable_warnings()
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    input_data = requests.get(url, cookies = {'session': session}, verify=False).text
    return input_data.split('\n')
