from pathlib import Path
from time import sleep

import requests
from tqdm import tqdm

endpoints = {
    "circuits": [
        "2022/10/circuits.json",
        "2022/99/circuits.json",
        "2022/circuits.json",
        "circuits/monaco.json",
        "constructors/red_bull/circuits.json",
        "constructors/red_bull/status/11/circuits.json",
        "drivers/alonso/circuits.json",
        "drivers/alonso/constructors/renault/circuits.json",
        "drivers/alonso/constructors/renault/grid/1/circuits.json",
        "drivers/alonso/constructors/renault/grid/1/results/1/circuits.json",
        "drivers/alonso/fastest/0/circuits.json",
        "drivers/alonso/fastest/1/circuits.json",
        "drivers/alonso/grid/11/circuits/monaco.json",
        "drivers/alonso/grid/1/circuits/monaco.json",
        "2023/status/23/circuits.json",
    ],
    "constructors": [
        "2019/20/constructors.json",
        "2019/99/constructors.json",
        "2019/constructors.json",
        "constructors/red_bull.json",
    ],
    "drivers": [
        "2018/1/drivers.json",
        "2018/99/drivers.json",
        "2018/drivers.json",
        "drivers/alonso.json",
        "2023/results/20/drivers.json",
    ],
    "laps": [
        "2013/18/laps.json?offset=45",
        "2013/1/laps.json",
        "2013/10/laps/1.json",
        "2023/1/drivers/leclerc/qualifying.json",
    ],
    "pitstops": [
        "2014/5/pitstops.json",
        "2014/5/pitstops.json?offset=30",
        "2014/10/pitstops/2.json",
        "2014/10/laps/7/pitstops.json",
    ],
    "qualifying": [
        "2015/13/qualifying.json",
        "2015/99/qualifying.json",
        "2015/qualifying.json",
        "constructors/red_bull/qualifying.json",
        "drivers/alonso/qualifying.json",
        "drivers/alonso/qualifying.json?offset=220",
        "2015/qualifying/1.json",
        "2015/grid/12/circuits/bahrain/qualifying/12.json",
        "2015/grid/12/circuits/bahrain/qualifying.json?limit=1",
        "2023/12/qualifying/1.json",
        "2023/12/qualifying/13.json",
        "2023/fastest/1/qualifying.json",
        "2023/status/1/qualifying.json",
        "2023/grid/1/qualifying.json",
    ],
    "races": [
        "2021/7/races.json",
        "2021/99/races.json",
        "2021/races.json",
        "2021.json",
        "2021/last.json",
        "2021/next.json",
    ],
    "results": [
        "2017/99/results.json",
        "2017/9/results.json",
        "2017/results.json",
        "constructors/red_bull/results.json?offset=15",
        "drivers/alonso/results.json",
        "2017/results/2.json",
        "2017/results/15.json",
        "2023/grid/1/results.json",
        "2023/status/1/results.json",
    ],
    "seasons": [
        "2023/5/seasons.json",
        "2023/99/seasons.json",
        "2023/seasons.json",
        "constructors/notexist/seasons.json",
        "constructors/red_bull/drivers/alonso/seasons.json",
        "constructors/red_bull/seasons.json",
        "drivers/alonso/constructors/renault/grid/1/results/1/seasons.json",
        "drivers/alonso/constructors/renault/grid/1/seasons.json",
        "drivers/alonso/constructors/renault/seasons.json",
        "drivers/alonso/constructors/renault/status/22/seasons.json",
        "drivers/alonso/fastest/0/seasons.json",
        "drivers/alonso/fastest/1/seasons.json",
        "drivers/alonso/grid/1/circuits/monaco/seasons.json",
        "drivers/alonso/seasons.json",
        "drivers/piastri/results/1/seasons.json",
        "drivers/russell/seasons.json",
        "grid/999/constructors/notexist/seasons.json",
        "constructors/brabham-ford/circuits/ain-diab/seasons.json",
    ],
    "sprint": [
        "2023/3/sprint.json",
        "2023/99/sprint.json",
        "2023/sprint.json",
        "2023/sprint/1.json",
        "constructors/red_bull/sprint.json",
        "drivers/alonso/sprint.json",
        "2023/sprint/17.json",
        "2023/grid/1/sprint.json",
        "2023/status/1/sprint.json",
    ],
    "status": [
        "2020/17/status.json",
        "2020/99/status.json",
        "2020/status.json",
        "2020/status/131.json",
        "constructors/red_bull/circuits/monaco/status.json",
        "constructors/red_bull/grid/1/status.json",
        "constructors/red_bull/results/11/status.json",
        "constructors/red_bull/status.json",
        "drivers/alonso/constructors/renault/status.json",
        "drivers/alonso/fastest/1/status.json",
        "drivers/alonso/status.json",
        "drivers/alonso/status/1.json",
    ],
    "driverstandings": [
        "2023/driverstandings.json",
        "2023/4/driverStandings.json",
        "2023/22/driverstandings.json",
        "1980/14/driverstandings.json?limit=21",
        "2023/22/driverstandings/1.json",
        "2016/4/driverstandings.json",
        "2016/5/driverstandings.json",
        "2023/drivers/alonso/driverstandings.json",
        "2023/4/driverStandings/22.json",
    ],
    "constructorstandings": [
        "2023/constructorstandings.json",
        "2023/1/constructorStandings.json",
        "2023/22/constructorstandings.json",
        "2023/13/constructorstandings.json",
        "2023/22/constructorstandings/1.json",
        "2023/constructors/alfa/constructorstandings.json",
        "2023/constructorStandings/12.json",
    ],
}

base_folder = Path("tests/fixtures/ergast_responses")
base_folder.mkdir(exist_ok=True)
for endpoint_type, test_urls in tqdm(endpoints.items()):
    folder = base_folder / endpoint_type
    folder.mkdir(exist_ok=True)
    for url in tqdm(test_urls, leave=False):
        file_path = folder / url.replace("/", "@").replace("?", "^")
        if file_path.exists():
            continue
        sleep(1)
        try:
            response = requests.get(f"http://ergast.com/api/f1/{url}", timeout=60)
        except Exception as ex:
            print(f"{url} had an exception: {ex}")
            continue
        if response.status_code != 200:
            print(f"{url} has non-200 status code: {response.status_code}")
            continue

        with open(file_path, "bw") as file:
            file.write(response.content)
