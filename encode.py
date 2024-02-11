import sys
import json
import base64

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
    with open(f"{directory}/{path}", "rb") as image:
        encoded = base64.b64encode(image.read())
        datatype = "jpg" if "jpg" in path.split(".")[-1].lower() else "png"
        url = f"data:image/{datatype};base64," + encoded.decode()

    html += (
        f'<img id="images/{path}" src="{url}"></img>\n'
        f'<p id="images/{path}/note">{data["images"][path]["note"]}</p>\n\n'
    )

html += "\n</body>"

with open(f"{directory}.html", "w") as f:
    f.write(html)
