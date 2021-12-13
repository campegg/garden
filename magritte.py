#!/usr/bin/env python
"""
Magritte - ceci n'est pas une static site generator.
Version: 0.0.0a1
"""


import argparse
import os
import shutil
import signal
import time
import watchdog
from dotenv import load_dotenv
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape
from markdown import Markdown
from multiprocessing import Event, Process
from operator import itemgetter
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# Project base directory
project_dir = Path(__file__).resolve().parent


# Site config
load_dotenv()
config = {
    "site_name": os.environ.get("SITE_NAME"),
    "publish_host": os.environ.get("PUBLISH_HOST"),
    "publish_user": os.environ.get("PUBLISH_USER"),
    "publish_dir": os.environ.get("PUBLISH_DIR"),
    "source_dir": project_dir / "source",
    "content_dir": project_dir / "content",
    "build_dir": project_dir / "build",
}


# Set Markdown options
md = Markdown(
    extensions=(
        "codehilite",
        "extra",
        "meta",
        "sane_lists",
        "smarty",
        "toc",
    ),
    extension_configs={
        "codehilite": {
            "linenums": True,
            "linespans": "line",
            "lineseparator": "<br>",
        },
    },
    output_format="html5",
)


# Set Jinja options
jinja = Environment(
    loader=PackageLoader("magritte", "source/templates"),
    autoescape=select_autoescape(
        enabled_extensions=("html"),
        default_for_string=True,
        default=True,
    ),
)


# Build the site
# Utility function to generate the menu
def build_menu(path=config["content_dir"]):
    menu = dict(name=Path(path).name, pages=[])
    tree = Path(path).iterdir()
    for branch in tree:
        leaf = Path(path) / branch
        if Path(leaf).is_dir():
            menu["pages"].append(build_menu(path=leaf))
            menu["pages"] = sorted(menu["pages"], key=lambda i: i["name"])
        else:
            source = md.convert(leaf.read_text())
            title = md.Meta["title"][0]
            menu["pages"].append(
                dict(
                    url=str(branch)
                    .replace(str(config["content_dir"]), "")
                    .replace(".md", ".html"),
                    name=title,
                )
            )
            menu["pages"] = sorted(menu["pages"], key=lambda i: i["name"])

    return menu


# Main build function
def build():
    # Empty the build directory
    try:
        for files in os.listdir(config["build_dir"]):
            path = os.path.join(config["build_dir"], files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
        print(f"{CLIColor.fmt('•', 'green')} Successfully emptied build directory")
    except:
        print(f"{CLIColor.fmt('•', 'red')} Failed to empty build directory")

    # Compile css
    css_input = f"{config['source_dir']}/styles/style.scss"
    css_output = f"{config['build_dir']}/assets/css/style.css"
    css = os.system(f"sass --style=compressed --no-source-map {css_input}:{css_output}")

    if css == 0:
        print(f"{CLIColor.fmt('•', 'green')} Successfully compiled CSS")
    else:
        print(f"{CLIColor.fmt('•', 'red')} Failed to compile CSS with code: {css}")

    # Transfer images to build
    img_source_dir = f"{config['source_dir']}/images"
    img_build_dir = f"{config['build_dir']}/assets/img"
    img = shutil.copytree(img_source_dir, img_build_dir)

    if img:
        print(f"{CLIColor.fmt('•', 'green')} Successfully copied images")
    else:
        print(f"{CLIColor.fmt('•', 'red')} Failed to copy images with code: {img}")

    # Render the content
    for path in Path(config["content_dir"]).rglob("*.md"):
        input_path = str(path)
        output_file = Path(
            input_path.replace(
                str(config["content_dir"]), str(config["build_dir"])
            ).replace(".md", ".html")
        )
        output_dir = Path(
            str(path.parent).replace(
                str(config["content_dir"]), str(config["build_dir"])
            )
        )

        source = md.convert(path.read_text())

        page_content = {}
        page_content["html"] = source
        page_content["title"] = md.Meta["title"][0]
        page_content["created"] = md.Meta["date"][0]
        page_content["updated"] = md.Meta["update"][0]
        page_content["site"] = config["site_name"]
        page_content["menu"] = build_menu()

        template = md.Meta["template"][0]
        output = jinja.get_template(f"{template}.html").render(page_content)

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output)
            print(
                f"{CLIColor.fmt('•', 'green')} Successfully wrote HTML to {output_file}"
            )
        except:
            print(
                f"{CLIColor.fmt('•', 'red')} Failed to write HTML file to {output_file}"
            )


# Run the dev server
# Utility function to create the server
def create_server():
    os.chdir(config["build_dir"])
    httpd = HTTPServer(("", 8888), SimpleHTTPRequestHandler)
    httpd.serve_forever()


# Start the dev server and watch for changes
def dev():
    class DevServer(FileSystemEventHandler):
        p = None

        def start_server(self):
            if self.p:
                self.stop_server()
            build()
            print(f"{CLIColor.fmt('•', 'green')} Starting server at 127.0.0.1:8888 (CTRL+C to stop)...\n  Watching {config['content_dir']}\n  Watching {config['source_dir']}")
            self.p = Process(target=create_server)
            self.p.start()

        def stop_server(self):
            if self.p:
                print(f"\n{CLIColor.fmt('•', 'red')} Stopping server...")
                self.p.terminate()
                pass
            else:
                print(f"{CLIColor.fmt('•', 'yellow')} No server to stop")

        def on_any_event(self, event):
            if (
                event.event_type == "created"
                or event.event_type == "modified"
                and event.is_directory == False
            ):
                self.stop_server()
                print(f"{CLIColor.fmt('•', 'yellow')} Rebuilding...")
                build()
                self.start_server()

    devserver = DevServer()

    observer = Observer()
    observer.schedule(devserver, config["source_dir"], recursive=True)
    observer.schedule(devserver, config["content_dir"], recursive=True)
    observer.start()

    try:
        devserver.start_server()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        devserver.stop_server()
        observer.stop()
    observer.join()


# Publish the site
def publish():
    build()
    try:
        os.system(
            f"rsync -avzuP --delete {config['build_dir']}/ {config['publish_user']}@{config['publish_host']}:{config['publish_dir']}"
        )
        print(
            f"{CLIColor.fmt('•', 'green')} Successfully published to {config['publish_host']}"
        )
    except:
        print(f"{CLIColor.fmt('•', 'red')} Failed to publish the site ;(")


# Utility class(es) to add color to console messages
class CLIColor:
    @classmethod
    def fmt(self, text, color):
        colors = {
            "red": "\u001b[1;31m",
            "yellow": "\u001b[1;33m",
            "green": "\u001b[1;32m",
        }
        self.text = text
        self.color = colors[color]
        self.end = "\u001b[0;0m"
        return f"{self.color}{self.text}{self.end}"


# Make it all go...
if __name__ == "__main__":

    commands = [
        ("-b", "--build", "Build your site locally."),
        ("-d", "--dev", "Run a local dev server to preview your work."),
        ("-p", "--publish", "Publish your site to the configured server."),
    ]

    parser = argparse.ArgumentParser()
    for command in commands:
        parser.add_argument(
            command[0], command[1], help=command[2], action="store_true"
        )
    arg = parser.parse_args()

    if arg.build:
        build()
    elif arg.dev:
        dev()
    elif arg.publish:
        publish()
    else:
        print(f"You've got to tell me what to do, yo.")
