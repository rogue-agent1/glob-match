#!/usr/bin/env python3
"""Glob pattern matching — *, ?, **, [chars], {alt1,alt2}."""
import sys, os, re

def glob_to_regex(pattern):
    i, n, result = 0, len(pattern), ""
    while i < n:
        c = pattern[i]
        if c == "*":
            if i+1 < n and pattern[i+1] == "*":
                result += ".*"; i += 2
                if i < n and pattern[i] == "/": result += "/?"; i += 1
            else: result += "[^/]*"
        elif c == "?": result += "[^/]"
        elif c == "[":
            j = i + 1
            while j < n and pattern[j] != "]": j += 1
            result += "[" + pattern[i+1:j] + "]"; i = j
        elif c == "{":
            j = i + 1
            while j < n and pattern[j] != "}": j += 1
            alts = pattern[i+1:j].split(",")
            result += "(" + "|".join(re.escape(a) for a in alts) + ")"; i = j
        else: result += re.escape(c)
        i += 1
    return "^" + result + "$"

def match(pattern, text): return bool(re.match(glob_to_regex(pattern), text))

def find(pattern, root="."):
    results = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            path = os.path.relpath(os.path.join(dirpath, f), root)
            if match(pattern, path): results.append(path)
    return results

def cli():
    if len(sys.argv) < 3:
        print("Usage: glob_match <pattern> <text|--find [root]>"); sys.exit(1)
    pat = sys.argv[1]
    if sys.argv[2] == "--find":
        root = sys.argv[3] if len(sys.argv)>3 else "."
        for p in sorted(find(pat, root)): print(p)
    else:
        text = sys.argv[2]
        print(f"Pattern: {pat}"); print(f"Text: {text}"); print(f"Match: {match(pat, text)}")
        print(f"Regex: {glob_to_regex(pat)}")

if __name__ == "__main__": cli()
