---
title: Using Magritte
template: page
date: 2021-12-13
update:
---

# Using Magritte

Magritte runs entirely on your local machine; it essentailly takes some Markdown-formatted content files and come SCSS styles and turns them into HTML and CSS that you can publish (or upload manually, if that's your thing) to a web server.

Before you start, make sure you have Dart Sass installed on your system and available on your `$PATH`. On a Mac, the easiest way to do this is via a package manager like [Homebrew](https://brew.sh): `$ brew install sass/sass/sass`. And if you want to be able to publish directly to a server, you'll need key-based SSH authentication set up. (You are using key-based authentication, aren't you? If you're not, you really should.)

1. Clone the repo: `$ git clone https://github.com/campegg/garden-v1.git && cd ./garden-v1` (it contains all of the content for this site; you'll probably want to get rid of that)
2. Set up and activate a virtual environment: `$ python3 -m venv venv` and `$ source venv/bin/activate`
3. Install the required packages: `(venv)$ pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and edit the variables:
    * `SITE_NAME` is what you'd like to call your site.
    * `PUBLISH_HOST` is where you want to publish to, e.g. `example.com`
    * `PUBLISH_USER` the username you use to log in to the server above.
    * `PUBLISH_DIR` the directory where you want to store the files on your server, e.g. `/var/www/html` (no trailing slash!)

From here, you have a few options:

* `(venv)$ python magritte.py -b` or `(venv)$ python magritte.py --build` will (surprise!) build the site locally so you can upload it via FTP or whatever.
* `(venv)$ python magritte.py -p` or `(venv)$ python magritte.py --publish` will build the site, then publish to the server you configured above.
* `(venv)$ python magritte.py -d` or `(venv)$ python magritte.py --dev` will build the site and start a local server at `http://127.0.0.1:8888` so you can check your work. This server watches the `content` and `source` directories, and will rebuild the site and restart the server when files change. It's 95% of the way there, but there are a couple of weirdnesses that I need to iron out, so manually stopping the server manually with `CTRL+C` and restarting might be necessary from time to time.
