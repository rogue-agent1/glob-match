#!/usr/bin/env python3
"""Glob pattern matching."""

def glob_match(pattern: str, text: str) -> bool:
    pi = ti = 0
    star_pi = star_ti = -1
    while ti < len(text):
        if pi < len(pattern) and pattern[pi] == '*':
            star_pi = pi; star_ti = ti; pi += 1
        elif pi < len(pattern) and (pattern[pi] == '?' or pattern[pi] == text[ti]):
            pi += 1; ti += 1
        elif pi < len(pattern) and pattern[pi] == '[':
            end = pattern.index(']', pi)
            chars = pattern[pi+1:end]
            negate = chars.startswith('!')
            if negate: chars = chars[1:]
            matched = False
            i = 0
            while i < len(chars):
                if i + 2 < len(chars) and chars[i+1] == '-':
                    if chars[i] <= text[ti] <= chars[i+2]: matched = True
                    i += 3
                else:
                    if chars[i] == text[ti]: matched = True
                    i += 1
            if matched != negate:
                pi = end + 1; ti += 1
            elif star_pi >= 0:
                pi = star_pi + 1; star_ti += 1; ti = star_ti
            else:
                return False
        elif star_pi >= 0:
            pi = star_pi + 1; star_ti += 1; ti = star_ti
        else:
            return False
    while pi < len(pattern) and pattern[pi] == '*':
        pi += 1
    return pi == len(pattern)

def filter_glob(pattern: str, items: list) -> list:
    return [item for item in items if glob_match(pattern, item)]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: glob_match.py <pattern> <text>"); sys.exit(1)
    print(glob_match(sys.argv[1], sys.argv[2]))

def test():
    assert glob_match("*.py", "test.py")
    assert not glob_match("*.py", "test.js")
    assert glob_match("test?", "test1")
    assert not glob_match("test?", "test12")
    assert glob_match("*", "anything")
    assert glob_match("", "")
    assert not glob_match("", "x")
    assert glob_match("a*b*c", "aXXbYYc")
    assert glob_match("[abc]", "b")
    assert not glob_match("[abc]", "d")
    assert glob_match("[a-z]", "m")
    assert not glob_match("[a-z]", "5")
    assert glob_match("[!0-9]", "a")
    assert not glob_match("[!0-9]", "5")
    # Filter
    files = ["test.py", "main.py", "readme.md", "config.json"]
    assert filter_glob("*.py", files) == ["test.py", "main.py"]
    print("  glob_match: ALL TESTS PASSED")
