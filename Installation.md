# Installation and Testing Guide 
### Create a Discord Bot
To create a Discord Bot, you must:
* have a [Discord Account](https://discord.com/login)
* have a Discord server for the bot
* create a Discord bot in the [Developer Portal](https://discord.com/developers/applications), but DO NOT ADD to your server yet ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
* create a `.env` file with your Bot Token and add this to your .gitignore (Discord will automatically regenerate your token if you accidentally upload it to Github)
    ```
    # .env
    DISCORD_TOKEN={your-bot-token}
    ```

NOTE: Run the bot before inviting it to your server in order for auto-initiate commands to run

This includes:
* Creating Instructor Role
* Adding server owner to Instructor Role
* Creating Bot channels

### Run Teacher's Pet Bot
To run the Teacher's Pet Bot:
1. Ensure you have the following installed:
    * [Python 3](https://www.python.org/downloads/) 
    * [pip](https://pip.pypa.io/en/stable/installation/)
    * [SQLite w/Tools](https://www.sqlite.org/download.html)
2. Clone this repo onto your local machine
3. In the repository directory, run `pip install -r src/requirements.txt`
4. Run `python src/bot.py` to start the bot
5. Invite the bot to your server ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
    * NOTE:  When using the OAuth2 URL Generator, make sure you check the box which gives your bot Administrative permissions

### Run Tests
To run tests on the Teacher's Pet Bot:
1. Create a second bot for testing
2. Add the Test Bot's token to the `.env` file
    ```
    # .env
    DISCORD_TOKEN={your-bot-token}
    TESTING_BOT_TOKEN={your-testing-bot-token}
    ```
 3. In `test/tests.py`, update the `TEST_GUILD_ID` to be the id of the server/guild you are testing in.
 4. Start Teacher's Pet Bot by running one of the following commands in the root directory of the project:
    * Without Coverage: `pytest src/bot.py`
    * With Coverage: `coverage run --source=./src -m pytest src/bot.py`
 5. Run the tests with `python test/tests.py` in the root directory of the project
 6. If you collected coverage, run `coverage report` to see coverage details.
