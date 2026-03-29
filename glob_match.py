#!/usr/bin/env python3
"""Glob Match - Unix-style glob pattern matching with ** support."""
import sys, os, re

def glob_to_regex(pattern):
    regex = "^"; i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == "*":
            if i + 1 < len(pattern) and pattern[i+1] == "*":
                regex += ".*"; i += 2
                if i < len(pattern) and pattern[i] == "/": i += 1
            else:
                regex += "[^/]*"
        elif c == "?": regex += "[^/]"
        elif c == "[":
            j = i + 1
            while j < len(pattern) and pattern[j] != "]": j += 1
            regex += "[" + pattern[i+1:j] + "]"; i = j
        elif c in ".+(){}|^$\\": regex += "\\" + c
        else: regex += c
        i += 1
    return regex + "$"

def match(pattern, text):
    return bool(re.match(glob_to_regex(pattern), text))

def find(pattern, root="."):
    results = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, root)
            if match(pattern, rel): results.append(rel)
    return sorted(results)

def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else "*.py"
    print(f"=== Glob Match ===\nPattern: {pattern}\n")
    tests = ["main.py", "src/app.py", "test/test_main.py", "README.md", "lib/utils.js",
             "src/components/Button.tsx", ".gitignore", "dist/bundle.min.js"]
    if len(sys.argv) <= 2:
        print("Regex:", glob_to_regex(pattern))
        print("\nTest matches:")
        for t in tests:
            m = match(pattern, t)
            print(f"  {'✓' if m else '✗'} {t}")
    else:
        root = sys.argv[2] if len(sys.argv) > 2 else "."
        results = find(pattern, root)
        print(f"Found {len(results)} match(es):")
        for r in results[:20]: print(f"  {r}")

if __name__ == "__main__":
    main()
