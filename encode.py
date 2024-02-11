import json
import base64
import argparse

parser = argparse.ArgumentParser(prog="Encode media")
parser.add_argument("directory")
parser.add_argument("-f", "--single-file", action="store_true")

args = parser.parse_args()
directory = args.directory
single_file = args.single_file

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
    if single_file:
        with open(f"{directory}/{path}", "rb") as image:
            encoded = base64.b64encode(image.read())
            datatype = "jpg" if "jpg" in path.split(".")[-1].lower() else "png"
            url = f"data:image/{datatype};base64," + encoded.decode()

        html += (
            f'<img id="images/{path}" src="{url}"></img>\n'
            f'<p id="images/{path}/note">{data["images"][path]["note"]}</p>\n\n'
        )
    else:
        html += (
            f'<img id="images/{path}" src="{path}"></img>\n'
            f'<p id="images/{path}/note">{data["images"][path]["note"]}</p>\n\n'
        )

html += "\n</body>"

if single_file:
    with open(f"{directory}.html", "w") as f:
        f.write(html)
else:
    with open(f"{directory}/index.html", "w") as f:
        f.write(html)
