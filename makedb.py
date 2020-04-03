# Create table with char and audio-file, sorted
# Chinese char
# pinyin number
# pinyin notation
# audio files

import re
import glob
import random
import json

audio_dirs = [
    "chi-balm-hsk1",
    "cmn-balm-congcong",
    "cmn-balm-hsk1",
    "cmn-caen-tan",
]

def strip_tags(t):
    return re.sub(r"<[^>]*>", "", t).strip()

chars = {}

for path in glob.glob("hanzidb/*"):
    with open(path) as fp:
        for line in fp:
            if line.startswith('<tr><td><a href="/character/'):
                parts = line.split("</td><td>")
                char = strip_tags(parts[0])
                pinyin = strip_tags(parts[1])
                hsk = strip_tags(parts[5])
                freq = strip_tags(parts[7])
                # print(char, pinyin, hsk, freq)
                chars[char] = {
                    "char": char,
                    "pinyin": pinyin,
                    "hsk": hsk,
                    "freq": freq
                }

with open("junda.txt") as fp:
    for line in fp:
        parts = line.split()
        if len(parts) < 5:
            continue

        serial = int(parts[0])
        char = parts[1]
        pinyin = parts[4].split("/")
        # print(serial, char, pinyin)
        if char in chars:
            chars[char].update({
                "serial": serial,
                "pinyin_alt": pinyin
            })

audio = {}
for audio_dir in audio_dirs:
    index = "audio/%s/flac/index.tags.txt" % audio_dir
    fname = None
    with open(index) as fp:
        for line in fp:
            if line.startswith('['):
                fname = line.strip("[]\r\n")
            if "=" in line:
                key, value = line.strip().split("=", 1)
                if key == "SWAC_TEXT":
                    if value not in audio:
                        audio[value] = []
                    audio[value].append("audio/%s/flac/%s" % (audio_dir, fname))
                    

for char, data in chars.items():
    if char in audio:
        data["audio"] = audio[char]

print(json.dumps(sorted([d for d in chars.values() if "serial" in d and "audio" in d], key=lambda d: d["serial"])))
