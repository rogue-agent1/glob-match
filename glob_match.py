#!/usr/bin/env python3
"""Glob pattern matcher from scratch (*, ?, [abc], **)."""
import sys

def glob_match(pattern, text, i=0, j=0):
    while i < len(pattern):
        if pattern[i] == '*':
            if i+1 < len(pattern) and pattern[i+1] == '*':
                i += 2
                if i < len(pattern) and pattern[i] == '/': i += 1
                for k in range(j, len(text)+1):
                    if glob_match(pattern, text, i, k): return True
                return False
            i += 1
            for k in range(j, len(text)+1):
                if k > j and text[k-1] == '/': break
                if glob_match(pattern, text, i, k): return True
            return False
        elif j >= len(text): return False
        elif pattern[i] == '?':
            if text[j] == '/': return False
            i += 1; j += 1
        elif pattern[i] == '[':
            end = pattern.index(']', i+1)
            chars = pattern[i+1:end]; neg = chars.startswith('!')
            if neg: chars = chars[1:]
            match = text[j] in chars
            if neg: match = not match
            if not match: return False
            i = end + 1; j += 1
        else:
            if pattern[i] != text[j]: return False
            i += 1; j += 1
    return j == len(text)

def main():
    if "--demo" in sys.argv:
        tests = [
            ("*.py", "hello.py", True), ("*.py", "dir/hello.py", False),
            ("**/*.py", "dir/hello.py", True), ("src/[ab]*.js", "src/app.js", True),
            ("test?.txt", "test1.txt", True), ("test?.txt", "test12.txt", False),
        ]
        for pat, text, expected in tests:
            result = glob_match(pat, text)
            status = "✓" if result == expected else "✗"
            print(f"{status} glob('{pat}', '{text}') = {result}")
    elif len(sys.argv) > 2:
        print(glob_match(sys.argv[1], sys.argv[2]))
if __name__=="__main__": main()
