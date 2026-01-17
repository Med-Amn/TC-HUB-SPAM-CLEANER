import os
import shutil
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "Input")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

FILES_TO_REMOVE = [
    "اقرأني.md",
    "ПРОЧТИМЕНЯ.md",
    "README_中文.md",
    "README.txt",
    "README.md",
    "LISEZMOI.md",
    "LÉAME.md",
    "Best FiveM Leaks Server.url"
]

TEXT_EXT = (".lua", ".js", ".css", ".html", ".py", ".txt")

SPAM_KEYWORDS = [
    "this file leaked",
    "tc hub",
    "tchub",
    "discord.gg",
    "join our server"
]

ASCII_PATTERN = re.compile(r"[░▒▓█]{2,}", re.UNICODE)
BYTCHUB_PATTERN = re.compile(r"-?bytcHub", re.IGNORECASE)

def clean_name(name: str) -> str:
    return BYTCHUB_PATTERN.sub("", name)

def is_spam_line(line: str) -> bool:
    lower = line.lower()
    if any(word in lower for word in SPAM_KEYWORDS):
        return True
    if ASCII_PATTERN.search(line):
        return True
    # lines just with -- or whitespace that are part of spam
    if re.fullmatch(r"\s*--\s*", line):
        return True
    # empty or whitespace lines at start
    if line.strip() == "":
        return True
    return False

def clean_content(lines):
    cleaned = []
    inside_block = False
    # Skip empty/spam lines at the very start
    i = 0
    while i < len(lines):
        if is_spam_line(lines[i].strip()):
            i += 1
        else:
            break
    # Process remaining lines
    for line in lines[i:]:
        stripped = line.strip()
        # Block comment start
        if stripped.startswith("--[[") or stripped.startswith("/*") or stripped.startswith("<!--"):
            inside_block = True
            cleaned.append(line)
            continue
        # Block comment end
        if (stripped.endswith("]]") or stripped.endswith("*/") or stripped.endswith("-->")) and inside_block:
            inside_block = False
            cleaned.append(line)
            continue
        if inside_block:
            # Inside block: remove spam inside block
            if not is_spam_line(stripped):
                cleaned.append(line)
            continue
        # Outside block: remove spam lines completely (including empty -- lines)
        if is_spam_line(stripped):
            continue
        # Keep all other lines (including normal comments)
        cleaned.append(line)
    return cleaned

def print_progress(current, total, bar_length=40):
    percent = current / total
    filled_len = int(bar_length * percent)
    bar = '█' * filled_len + '-' * (bar_length - filled_len)
    sys.stdout.write(f'\rProgress: |{bar}| {percent*100:6.2f}% ({current}/{total})')
    sys.stdout.flush()

def count_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        count += len(files)
    return count

def process():
    total_files = count_files(INPUT_DIR)
    processed = 0

    for root, dirs, files in os.walk(INPUT_DIR):
        rel_path = os.path.relpath(root, INPUT_DIR)
        out_dir = OUTPUT_DIR if rel_path == "." else os.path.join(OUTPUT_DIR, *[clean_name(p) for p in rel_path.split(os.sep)])
        os.makedirs(out_dir, exist_ok=True)

        for file in files:
            processed += 1
            print_progress(processed, total_files)

            if file in FILES_TO_REMOVE:
                continue

            src = os.path.join(root, file)
            dst = os.path.join(out_dir, clean_name(file))

            if file.lower().endswith(TEXT_EXT):
                with open(src, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                cleaned = clean_content(lines)

                with open(dst, "w", encoding="utf-8") as f:
                    f.writelines(cleaned)
            else:
                shutil.copy2(src, dst)

    print("\n✅ DONE: spam removed, empty -- lines removed, code starts at first line, block comments preserved, ByTcHub renamed")

if __name__ == "__main__":
    if not os.path.exists(INPUT_DIR):
        print("❌ Input folder ma kaynach")
    else:
        process()
