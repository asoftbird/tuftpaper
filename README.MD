usage: 
set up a scheduler to run `run.bat` hourly, preferably at least 5 minutes after the bot has posted. 
you will need a twitter dev account with auth/consumer keys and a bearer token, put these in `.env` and use the key names as described in `.env template`

the images will be dropped in `/img/`. then set your background to slideshow and point it to that folder. 

you might not want to run this for years on end as hourly bots will post 24*365= ~9000 images yearly. 
it'll also download at full resolution! 

also it miiiiiight whine about `./img/`  and `./log.txt` not existing, just create those if it does that. 


you can change which account it pulls from in `config.json`; account-name is the user @, log-file points to the log, output-dir to the place where images will be saved and timezone-modifier adds or subtracts hours in a hacky way to correct for timezones. i'm in gmt+2 so it's 2 by default :>