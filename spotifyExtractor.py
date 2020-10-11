import os
import sys

CLI_ID = "c031db81e9e841c382309dac036c36ae"
CLI_SEC = os.environ.get("spotifyDiscordBotSecret")
if CLI_SEC is None:
    print("You have not added the spotify Client secret as an environment variable. Exiting.")
    sys.exit()



