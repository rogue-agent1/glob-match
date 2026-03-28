#!/usr/bin/env python3
"""glob_match - Unix glob pattern matching without fnmatch."""
import sys, os, re

def glob_to_regex(pattern):
    i, n, res = 0, len(pattern), ""
    while i < n:
        c = pattern[i]
        if c == "*":
            if i+1 < n and pattern[i+1] == "*":
                res += ".*"; i += 2
                if i < n and pattern[i] == "/": res += "/?"; i += 1
                continue
            res += "[^/]*"
        elif c == "?": res += "[^/]"
        elif c == "[":
            j = i+1
            while j < n and pattern[j] != "]": j += 1
            res += "[" + pattern[i+1:j] + "]"; i = j
        elif c in ".+^${}()|\\": res += "\\" + c
        else: res += c
        i += 1
    return "^" + res + "$"

def match(pattern, text):
    return bool(re.match(glob_to_regex(pattern), text))

def glob_files(pattern, root="."):
    results = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            path = os.path.relpath(os.path.join(dirpath, f), root)
            if match(pattern, path): results.append(path)
    return sorted(results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: glob_match.py <pattern> [root] [--test text]"); sys.exit(1)
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        print("match" if match(sys.argv[1], sys.argv[idx+1]) else "no match")
    else:
        root = sys.argv[2] if len(sys.argv) > 2 else "."
        for f in glob_files(sys.argv[1], root): print(f)
