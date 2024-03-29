import os
import os.path
import json
import requests
import re

from PIL import Image

with open("./themes.json") as f:
    themes = json.load(f)["themes"]

with open("./README_TEMPLATE.md") as f:
    readme = f.read()

def gen_readme(name,repo,branch,img_files,img_urls):
    r = f"""
# {name}
### {repo}

### images:

"""
    if img_urls:
        r += f"\n![{name}]({img_urls[0]})\n"
    elif img_files:
        r += f"\n{repo}/blob/{branch}/{img_files[0]}?raw=true\n"
    return r



def find_image_files(path):
    images = []
    for file in os.listdir(path):
        if "wall" in file:
            continue
        if os.path.isdir(os.path.join(path,file)):
            images.extend(find_image_files(os.path.join(path,file)))
        if str(file).endswith(".jpg") or str(file).endswith(".png"):
            images.append(os.path.join(path,file))
    return images

def find_image_readme(rdme):
    urls = []
    print(rdme)
    imgs = re.findall("(https:\/\/.*\.(png|jpg|gif))",rdme)
    print("====")
    print(imgs)
    for url in imgs:
        if len(url) > 1: urls.append(url[0])
    return urls

def find_img_tags(rdme):
    urls = []
    imgs = re.findall("<img.*src=\"(.*?)\"",rdme)
    for url in imgs:
        if url.startswith("http"): urls.append(url)
    return urls

def find_urls(rdme):
    md = find_image_readme(rdme)
    html = find_img_tags(rdme)

    # fetch image and sort on size
    images = {}
    for i,url in enumerate([*md,*html]):
        im = requests.get(url)
        if im.status_code == 200:
            #check if image is valid
            #save img to /tmp
            with open(f"/tmp/{i}","wb") as f:
                f.write(im.content)
            try:
                im = Image.open(f"/tmp/{i}")
            except:
                print("error opening image")
                continue
            images[url] = sum(im.size)
        else:
            print("error fetching image")
    
    # sort images
    images = sorted(images.items(), key=lambda x: x[1], reverse=True)
    print(images)
    return [x[0] for x in images]

with open("./themes.json","r") as f:
    themes_json = json.load(f)

for theme in themes:
    path = f'themes/{theme["name"].split("/")[-1]}'
    image_files = find_image_files(path)
    content = ""
    if os.path.isfile(os.path.join(path,"readme.md")):
        with open(os.path.join(path,"readme.md")) as f:
            content = f.read()
    elif os.path.isfile(os.path.join(path,"./README.md")):
        with open(os.path.join(path,"README.md")) as f:
            content = f.read()
    urls = find_urls(content)

    print("files :: ")
    print(image_files)
    print("urls ::")
    print(urls)

    txt = gen_readme(theme["name"],theme["repo"],theme["branch"],image_files,urls)
    
    for t in themes_json["themes"]:
        if t["name"] == theme["name"]:
            t["images"] = urls

    readme += f"\n{txt}\n <hr>\n"

with open("./README.md","w") as f:
    f.write(readme)

with open("./themes.json","w") as f:
    json.dump(themes_json,f,indent=4)



