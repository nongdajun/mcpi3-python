import re
import os

java_file = r"D:\Ga\MC\开发\mywork\mcpi3-mod\src\main\java\com\nongdajun\mcpi3\api\Commands.java"

if not os.path.exists(java_file):
    exit("file not found")

with open(java_file, "r") as f:
    code = f.read()


def parse_type(t):
    global code
    mask = re.findall(f"{t}CommandMask[\\s]*=[\\s]*(.+?);", code)[0]
    mask = int(mask, 16)

    ret = re.findall(f"public[\\s]+enum[\\s]+{t}[\\s]*{{(.+?)}}", code, re.M|re.DOTALL)[0]
    arr = ret.strip().split("\n")
    arr = [a.strip().strip(',') for a in arr]
    arr = [a for a in arr if a]

    return mask, arr


def format_name(n):
    arr = n.split("_")
    for i, a in enumerate(arr):
        if i:
            arr[i] = a.capitalize()
        else:
            arr[i] = a.lower()
    return "".join(arr)


types = ['Common', 'Server', 'Client']
for t in types:
    mask, arr = parse_type(t)
    assert mask and arr
    print(f"# --- {t} command function mapping start---")
    for i, a in enumerate(arr):
        if a.startswith("__") and a.endswith("__"):
            continue
        print(f"    {format_name(a)} = {a}")
    print(f"# --- {t} command function mapping end---\n")





