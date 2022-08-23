usage: 
set up a scheduler to run `run.bat` hourly, preferably at least 5 minutes after the bot has posted. 
you will need a twitter dev account with auth/consumer keys and a bearer token, put these in `.env` and use the key names as described in `.env template`

the images will be dropped in `./img/`. then set your background to slideshow and point it to that folder. 
set up a scheduler to run `cleanup.bat` every day so it archives older images. by default it'll keep all images from today unless there's less than 8, as it'll then include those from yesterday as well.
images won't be deleted but will be moved to `./archive/`. 


it'll also download at full resolution! 

also it miiiiiight whine about `./img/`, `./archive/` and `./log.txt` not existing, just create those if it does that. 


you can change which account it pulls from in `config.json`; account-name is the user @, log-file and log-file-cleanup point to the log / cleanup log, output-dir and archive-dir to the place where images will be saved and archived. i'm in gmt+2 so it's 2 by default :>
