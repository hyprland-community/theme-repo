import os
import os.path
import json
import re

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
        if len(img_urls) >= 2:
            img_urls = img_urls[:2]
        for img in img_urls:
            r += f"![{name}]({img})\n"
    elif img_files:
        if len(img_files) >= 2:
            img_files = img_files[:2]
        for img in img_files:
            r += f"{repo}/blob/{branch}/{img}?raw=true\n"
    
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

for theme in themes:
    path = f'themes/{theme["repo"].split("/")[-1]}'
    image_files = find_image_files(path)
    content = ""
    if os.path.isfile(os.path.join(path,"readme.md")):
        with open(os.path.join(path,"readme.md")) as f:
            content = f.read()
    elif os.path.isfile(os.path.join(path,"./README.md")):
        with open(os.path.join(path,"README.md")) as f:
            content = f.read()
    urls = find_image_readme(content)

    print("files :: ")
    print(image_files)
    print("urls ::")
    print(urls)

    txt = gen_readme(theme["name"],theme["repo"],theme["branch"],image_files,urls)

    readme += f"\n{txt}\n <hr>\n"

with open("./README.md","w") as f:
    f.write(readme)




