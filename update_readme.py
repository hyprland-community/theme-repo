import os
import os.path
import json
import re

with open("./themes.json") as f:
    themes = json.load(f)["themes"]

readme = """
# theme-repo

to add your theme to this repo, open an issue with the `Add Theme` form template

# How do I more easily browse themes?
Check out the site: [theme browser](https://hyprland-community.github.io/themes.html) (site still WIP)

# how do i install these themes?

check out the tool [hyprland-community/hyprtheme](https://github.com/hyprland-community/hyprtheme)
```bash
hyprtheme repo install <theme-name>
```

# help, how do i make and submit a theme?
✨ [wiki](https://github.com/hyprland-community/theme-repo/wiki) ✨ 
> currently wip

<hr>

"""

def gen_readme(name,repo,img_files,img_urls):
    r = f"""
# {name}
### {repo}

### images:

"""
    if img_urls:
        for img in img_urls:
            r += f"![{name}]({img})"
    elif img_files:
        for img in img_files:
            r += f"{repo}/blob/{repo}/{img}?raw=true"
    
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

def find_image_readme(content:str):
    urls = []
    imgs = re.findall("(https:\/\/.*\.(png|jpg|gif))",content)
    print("====")
    print(imgs)
    for url in imgs:
        if len(url) > 1: urls.append(url[0])
    return urls

for theme in themes:
    path = theme["repo"].split("/")[-1]
    image_files = find_image_files(path)
    content = ""
    if os.path.isfile("./readme.md"):
        with open("./readme.md") as f:
            content = f.read()
    elif os.path.isfile("./README.md"):
        with open("./README.md") as f:
            content = f.read()
    urls = find_image_readme(content)

    print("files :: ")
    print(image_files)
    print("urls ::")
    print(urls)

    txt = gen_readme(theme["name"],theme["repo"],image_files,urls)

    readme += f"\n{txt}\n <hr>\n"

with open("./README.md","w") as f:
    f.write(readme)




