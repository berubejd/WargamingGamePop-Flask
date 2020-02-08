# Wargaming Game Server Population - Flask

This Flask app is an update to my [Wargaming Game Population](https://github.com/berubejd/WargamingGamePop) console application from December 2019.  It incorporates the API calls made by that application into a background task managed by the [Advanced Python Scheduler](https://apscheduler.readthedocs.io/en/stable/) which has been integrated with Flask ([Flask-APSchedule](https://github.com/viniciuschiele/flask-apscheduler)).

The [Wargaming API](https://developers.wargaming.net) is queried via the defined background task in order to collect and store their world-wide server populations.  This data is stored into and queried from a DB using [SQLAlchemy](https://www.sqlalchemy.org/) and display using [PyGal](http://www.pygal.org/).

I kicked off this Flask project using the [Flask-Starter](https://github.com/berubejd/Flask-Starter) project I built previously.

## Screenshot

![Wargaming WoT Flask Screenshot](images/wotf.png?raw-true)

## API Access
The API request is sent to all four current regions: NA, EU, RU, and Asia.  While a relatively simple JSON structure, the resulting response for each region that needs to be parsed looks like:

```json
{
    "status": "ok",
    "data": {
        "wotb": [
            {
                "players_online":9999,
                "server":"NA"
            }
        ],
        "wot": [
            {
                "players_online":9999,
                "server":"303"
            }
        ],
        "wows": [
            {
                "players_online":9999,
                "server":"NA"
            }
        ]
    }
}
```

## Configuration
This application requires an API key which should be stored in the environment with a small number of other values.  The necessary key can be generated on the [Wargaming developer portal](https://developers.wargaming.net/applications/).
