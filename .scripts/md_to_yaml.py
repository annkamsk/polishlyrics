import glob, re
from typing import Dict

def parse_header(data: str):
    header_dict = {}

    match = re.search(r"---\s*(.+\n)+\s*---", data, re.M)
    if not match:
        return {}, -1
    
    header = match.group(0)
    last_pos = data.find(header) + len(header)

    value_regex = r"_?([^_]+)_?\s*\n"  # value with optional _ and a new line

    match = re.search(r"_?From_?: " + value_regex, header, re.M)
    header_dict["musical"] = match.group(1) if match else None
    
    match = re.search(r"_?Title_?: " + value_regex, header, re.M)
    header_dict["orig_title"] = match.group(1) if match else None

    match = re.search(r"_?By_?: " + value_regex, header)
    header_dict["by"] = match.group(1) if match else ""

    match = re.search(r"_?Translated_?: " + value_regex, header)
    header_dict["translated"] = match.group(1) if match else ""

    match = re.search(r"_?SourceLang_?: " + value_regex, header)
    header_dict["source_lang"] = match.group(1) if match else ""

    match = re.search(r"_?TargetLang_?: " + value_regex, header)
    header_dict["target_lang"] = match.group(1) if match else ""

    return header_dict, data[last_pos:].strip()

def parse_text_line(line: str):
    line = line.replace("\\", "")
    if not line.endswith("\n"):
        line += "\n"
    return line

def parse_file(data: str):
    header, text = parse_header(data)

    match = re.search(r"# (.+)\s*\n", data, re.MULTILINE)
    title = match.group(1) if match else None

    if not all([title, header.get("musical"), header.get("orig_title")]):
        return

    lines = text.split("\n")
    target_lyrics = [parse_text_line(line) for line in lines]

    head_sep = "---"
    with open(f"yaml/{'-'.join(header['musical'].split())}_{'-'.join(title.split())}.yml", "w+") as f:
        lines = "\n".join([
            head_sep, 
            f"title: {title}",
            f"from: {header['musical']}",
            f"orig_title: {header['orig_title']}",
            f"lyrics_by: {header['by']}",
            f"translated_by: {header['translated']}",
            f"source_lang: {header['source_lang']}",
            f"target_lang: {header['target_lang']}",
            head_sep,
            "\n"
        ])
        
        f.writelines([*lines, "target: |\n", "\t" + "\t".join(target_lyrics), "source: |"])


for file in glob.glob("*.md"):
    if file == "README.md":
        continue
    with open(file) as f:
        data = f.read()
        parse_file(data)