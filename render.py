import sys
import json

directory = sys.argv[1]
data = json.load(open(f"{directory}/data.json", "r"))

metadata = data["metadata"]

html = (
    """
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: monospace;
        }
        img {
            max-width: 600px;
            width: 100%;
        }
    </style>
</head>

<body>

"""
    f'<h1 id="metadata/title">{metadata["title"]}</h1>\n'
    f'<p id="metadata/description">{metadata["description"]}</p>\n'
    f'<p id="metadata/tag">{metadata["tag"]}</p>\n\n'
)

for path in data["images"]:
    html += (
        f'<img id="images/{path}" src="{path}"></img>\n'
        f'<p id="images/{path}/note">{data["images"][path]["note"]}</p>\n\n'
    )

html += "</body>"

with open(f"{directory}/index.html", "w") as f:
    f.write(html)
