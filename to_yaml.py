import glob, re

def parse_file(data):
    match = re.search(r"# (.+)\n", data[0])
    title = match.group(1) if match else None

    match = re.search(r"_?From_?: _(.+)_", data[1])
    musical = match.group(1) if match else None
    
    match = re.search(r"_?Title_?: _(.+)_", data[2])
    orig_title = match.group(1) if match else None

    match = re.search(r"_?By_?: _(.+)_", data[3])
    by = match.group(1) if match else None

    if not all([title, musical, orig_title]):
        return

    head_sep = "---"
    with open(f"yaml/{'-'.join(musical.split())}_{'-'.join(title.split())}.yml", "w+") as f:
        lines = "\n".join([
            head_sep, 
            f"title: {title}",
            f"from: {musical}",
            f"orig_title: {orig_title}",
            f"lyrics_by: {by}",
            "source_lang: en",
            "target_lang: pl",
            head_sep,
            "\n"
        ])
        f.writelines([*lines, "target: |\n", "\t".join(data[4:]), "source: |"])


for file in glob.glob("*.md"):
    if file == "README.md":
        continue

    with open(file) as f:
        data = f.readlines()
        parse_file(data)
