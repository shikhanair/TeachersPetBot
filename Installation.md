#Installation Guide
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
6. Invite the bot to your server ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/))
    * NOTE:  When using the OAuth2 URL Generator, make sure you check the box which gives your bot Administrative permissions
