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






f = open("../commands.py", "w")
types = ['Common', 'Server', 'Client']
for t in types:
    mask, arr = parse_type(t)
    assert mask and arr
    f.write(f"# {t} command codes \n")
    f.write(f"{t}CommandMask = {hex(mask)}\n")
    f.write("\n\n")
    f.write(f"class {t}:\n")
    for i, a in enumerate(arr):
        f.write(f"    {a} = {hex(mask|i)}\n")
    f.write("\n\n")
f.close()




