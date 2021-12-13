---
title: About Magritte
template: page
date: 2021-12-12
update:
---

# About Magritte

<i>Ceci n'est pas une static site generator</i>

I settled on the name "Magritte" as a kind of play on René Magritte's painting, [_The Treachery of Images_](https://en.wikipedia.org/wiki/The_Treachery_of_Images). While the thing I am building does generate a static site, it's not a static site generator in the same way as something like [Eleventy](https://www.11ty.dev) (or [Gatsby](https://www.gatsbyjs.com) or [Hugo](https://gohugo.io) or [Pelican](https://blog.getpelican.com) or [Jekyll](https://jekyllrb.com)) is; I'm not building something to generate _a_ site so much as I'm building something to generate _this_ site.

## Basic functional requirements:

* Markdown for content
{.complete}
* SCSS for styling
{.complete}
* Publish from the command line
{.complete}
* Local dev server that watches for changes (working, but with some weirdness)
{.in-progress}

## Other (pretty loose) requirements

* As few app files as possible (currently 1... can't go less than that, I guess)
* As few external---i.e. non-standard library---packages as possible (currently 8; 5 explicitly installed, 3 dependencies):
    1. importlib-metadata==4.8.2
    2. Jinja2==3.0.3
    3. Markdown==3.3.6
    4. MarkupSafe==2.0.1
    5. Pygments==2.10.0
    6. python-dotenv==0.19.2
    7. watchdog==2.1.6
    8. zipp==3.6.0
* No JavaScript (not that JS is inherently bad, but in the interests of simplicity I just don't want to use it)
