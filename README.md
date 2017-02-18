# Reddit wallpaper getter

Run this script at startup to set your background to a random image from reddit, by default using /r/wallpapers on a Windows Computer (except XP).

**Note**: Reddit sometimes throttles requests to it's json API, or sometimes the request times out. Try again if it fails to work.

**Note2**: It takes the source image of the post preview image, so NSFW posts will probably not work (but I don't know I haven't tried)

**Note3**: No resolution matching, the original has it, this is a worse version. I'm sorry but I didn't want to limit myself to imgur links.

## Requirements:

* Python 2.7+ or 3
* Pillow

## Usage:

You can just run:

    python reddit_wallpaper_getter.py

Output of --help:

<pre>
usage: reddit_wallpaper_getter.py [-h] [--destination DESTINATION]
                                  [--overwrite-existing OVERWRITE_EXISTING]
                                  [--output-name OUTPUT_NAME]
                                  [--reddit-json-url REDDIT_JSON_URL]
                                  [--set-wallpaper SET_WALLPAPER]

Use reddit for wallpapers

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION
                        Destination directory (default: /home/b/.r_wallpapers)
  --overwrite-existing OVERWRITE_EXISTING
                        Overwrite file if exists? (True / False), default is
                        False
  --output-name OUTPUT_NAME
                        Output filename (defaults to imgur name)
  --reddit-json-url REDDIT_JSON_URL
                        Specify a subreddit .json url. (default http://www.red
                        dit.com/r/wallpapers/top.json?t=week&limit=50)
  --set-wallpaper SET_WALLPAPER
                        Set wallpaper? (True / False), default is True

</pre>
