#! /usr/bin/python3
import sys
from datetime import datetime
import feedparser
import jinja2

feeds = sys.stdin.read()
entries = []
for feed in feeds.split():
    print("Fetching {}".format(feed), end=" ", file=sys.stderr)
    sys.stderr.flush()
    f = feedparser.parse(feed)
    print("Done", file=sys.stderr)
    for entry in f["entries"]:
        entries.append(
            {
                "published_parsed": entry["published_parsed"],
                "published": entry["published"],
                "title": entry["title"],
                "link": entry["links"][0]["href"],
            }
        )
tmplt = """
<html>
    <head>
        <title>feedreader</title>
    </head>
    <style>
    div{
            margin:auto;
            width:50%;
            
    }
    a {
            padding: 10px;
    }
    </style>
    <body>
        <p> Generated on {{ generated_time }} </p>
        {% for entry in entries %}
        <div>{{ entry["published"] }}<a href={{entry["link"]}}>{{entry["title"]}}</a></div>
        {% endfor %}
    </body>
</html>
"""
jinja_env = jinja2.Environment()
template = jinja_env.from_string(tmplt)
print(
    template.render(
        entries=sorted(entries, key=lambda x: x["published_parsed"], reverse=True),
        generated_time=str(datetime.now()),
    )
)
