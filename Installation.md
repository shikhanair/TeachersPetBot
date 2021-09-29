#Installation Guide
To create a Discord Bot, you must:
* have a [Discord Account](https://discord.com/login)
* have a Discord server for the bot
* create a Discord bot in the [Developer Portal](https://discord.com/developers/applications) and invite the bot to your server ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
* create a `.env` file with your Bot Token
    ```
    # .env
    DISCORD_TOKEN={your-bot-token}
    ```

To run the Teacher's Pet Bot:
1. Ensure you have the following installed:
    * [Python 3](https://www.python.org/downloads/) 
    * [pip](https://pip.pypa.io/en/stable/installation/)
    * [SQLite w/Tools](https://www.sqlite.org/download.html)
2. Clone this repo onto your local machine
3. In the repository directory, run `pip install -r src/requirements.txt`
4. Set up the database:
    * `sqlite3` to open sqlite from the command prompt
    * `.cd <DIRECTORY>` make sure you are in the root directory of the project
    * `.open db.sqlite` open existing database
    * `.read src/init_db.sql` initialize database with tables
5. Run `python src/bot.py` to start the bot