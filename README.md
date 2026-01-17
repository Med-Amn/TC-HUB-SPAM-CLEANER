# Tc Hub Spam Cleaner Tool

**Author:** Amn

---

## Description

This is a Python tool designed to **clean text and code files** from unwanted spam, ASCII art, and leak messages, specifically targeting files related to TC HUB, Discord links, and other spam content. It also:

- Removes spam files completely.  
- Removes spam lines from code, including empty comment lines (e.g., `--`) at the start of files.  
- Preserves **block comments** (`--[[ ]]`, `/* */`, `<!-- -->`).  
- Keeps normal comments within the code (`--`, `//`, `#`).  
- Renames files and folders to remove `ByTcHub`.  
- Supports multiple text and code languages (`.lua`, `.js`, `.css`, `.html`, `.py`, `.txt`).  
- Shows a **progress bar** to track processing.

---

## Installation

1. Make sure you have **Python 3.7+** installed.  
2. Clone or download this repository.  
3. Create an `Input` folder in the project directory and place all your files/folders inside it.  
4. Ensure an empty `Output` folder exists (it will store cleaned files).

---

## Usage

Run the script with:

```bash
python files.py
