# Cam's Digital Garden 🌱

This repo contains the content for my digital garden, along with the tool I have built to manage it--more details [here](https://campegg.net/magritte/index.html). Feel free to have a play with it; it's a bit messy, but it more-or-less works. It probably won't do anything awful, but in the event that any of this bricks your computer, emails dirty jokes to your grandma and/or punches your dog in the face, that's all on you.

Before you start, make sure you have Dart Sass installed on your system and available on your `$PATH`. If you're on a Mac, the easiest way to do this is via a package manager like [Homebrew](https://brew.sh): `$ brew install sass/sass/sass`. And if you want to be able to publish directly to a server, you'll need key-based SSH authentication set up. (You are using key-based authentication, aren't you? If you're not, you really should be.)

1. Clone this repo: `$ git clone https://github.com/campegg/garden-v1.git && cd ./garden-v1`
2. Set up and activate a virtual environment: `$ python3 -m venv venv` and `$ source venv/bin/activate`
3. Install the required packages: `(venv)$ pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and edit the variables:
    * `SITE_NAME` is what you'd like to call your site.
    * `PUBLISH_HOST` is where you want to publish to, e.g. `example.com`
    * `PUBLISH_USER` the username you use to log in to the server above.
    * `PUBLISH_DIR` the directory where you want to store the files on your server, e.g. `/var/www/html` (no trailing slash!)

From here, you have a few options:

* `(venv)$ python magritte.py -b` or `(venv)$ python magritte.py --build` will (surprise!) build the site locally.
* `(venv)$ python magritte.py -p` or `(venv)$ python magritte.py --publish` will build the site, then publish to the server you configured above.
* `(venv)$ python magritte.py -d` or `(venv)$ python magritte.py --dev` will build the site and start a local server at `http://127.0.0.1:8888` so you can check your work. This server watches the `content` and `source` directories, and will rebuild the site when files change. It's 95% of the way there, but there are a couple of weirdnesses that I need to iron out, so manually stopping the server manually with `CTRL` + `C` and restarting might be necessary from time to time.

## Contributing

I'm really only building this for me, but am always open to learning from people who know more than me, so if you have any suggestions or whatever, please feel free to send me a PR.

## License

This work is © 2021 and licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode). See [LICENSE](/LICENSE.md) for details.
