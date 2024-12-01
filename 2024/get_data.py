import requests
import urllib3
from session import session

urllib3.disable_warnings()


def save_data(year=2024, day=1):
    urllib3.disable_warnings()
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    input_data = requests.get(url, cookies={"session": session}, verify=False).text

    f = open(f"day{day:02d}.txt", "w")
    f.write(input_data)
    f.close()
    return


save_data()
