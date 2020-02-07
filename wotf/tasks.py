import json
import requests

from collections import defaultdict
from datetime import datetime
from flask import current_app as app

from . import db
from .models import Population_Data

from . import scheduler


def request_data(api_key):
    """ Request server info from Wargaming API and return Dict containing data from each region """

    # Current (20191213) list of regions and their associated TLDs
    regions = [
        ("na", "com"),
        ("ru", "ru"),
        ("eu", "eu"),
        ("asia", "asia"),
    ]  # (region, tld)

    data = defaultdict(dict)

    with requests.Session() as s:
        for region, tld in regions:
            r = s.get(
                f"https://api.worldoftanks.{tld}/wgn/servers/info/?application_id={api_key}&language=en"
            )

            if r.status_code == 200:
                api_resp = json.loads(r.text)

                data[region] = api_resp

    return dict(data)


def parse_data(data: dict, game_abbr: str = None):
    """ Parse data returned from request_data() and return regional totals """

    totals = defaultdict(lambda: defaultdict(int))

    for region_name, region_info in data.items():
        for game, game_servers in region_info["data"].items():

            if game_abbr and not game_abbr == game:
                continue

            for server in game_servers:
                # Populate region totals
                totals[region_name]["user_count"] += int(server["players_online"])
                totals[region_name]["server_count"] += 1

    return dict(totals)


@scheduler.task("cron", id="collect_data", minute="*/5")
def collect_data():
    with scheduler.app.app_context():
        print(f"Running test job at {datetime.now()}")
        api_key = app.config["API_KEY"]

        region_data = request_data(api_key)
        game_info = parse_data(region_data, "wot")

        for region, region_data in game_info.items():
            region_name = region.upper()
            region_count = region_data["user_count"]

            new_pop = Population_Data(region=region_name, count=region_count)

            db.session.add(new_pop)

        db.session.commit()
        print("Population data written to DB.")
