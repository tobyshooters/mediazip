import os
import argparse
import bs4
import json
import base64

data = {}

parser = argparse.ArgumentParser(prog="Decode media")
parser.add_argument("filename")

args = parser.parse_args()
filename = args.filename

target = filename.split(".")[0] + "-decoded"
if not os.path.exists(target):
    os.mkdir(target)


with open(filename, "r") as f:
    s = f.read()

html = bs4.BeautifulSoup(s, 'lxml')
for node in html.body.children:
    if isinstance(node, bs4.Tag) and node.get("id"):
        path = node["id"].split("/")

        leaf = data
        for k in path[:-1]:
            leaf[k] = leaf.get(k, {})
            leaf = leaf[k]

        if node.name == "img":
            leaf[path[-1]] = {"data": len(node["src"])}

            img = base64.b64decode(node["src"].split(",")[1].encode())
            with open(f"{target}/{path[-1]}", "wb") as f:
                f.write(img)

        else:
            leaf[path[-1]] = node.string

print(data)

with open(f"{target}/data.json", "w") as f:
    json.dump(data, f, indent=2)
