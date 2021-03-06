# Strava Telegram Bot

A simple Strava bot using Stravlib & Telegram for fetching and calculating statistics. App is ready to be deployed on Heroku. Attach a Postgres Database to the app before using.

### Prerequisites

1. pip
2. stravalib
3. python-telegram-bot
4. psycopg2-binary
5. requests

```
$ apt-get install python-pip
$ pip install stravalib
$ pip install python-telegram-bot
$ pip install psycopg2-binary
$ pip install requests
```

##### Deploy Hooks HTTP URL
```
https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={{app}}%20({{release}})%20deployed!
```

# Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/panchambharadwaj/strava-telegram-bot)

# Telegram Bot
[![Open](https://telegram.org/img/t_logo.png)](https://t.me/cadence90_bot)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/panchambharadwaj/strava-telegram-bot/blob/master/LICENSE) file for details