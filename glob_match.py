#!/usr/bin/env python3
"""Glob pattern matcher — supports *, ?, [abc], [!abc], **, {a,b}.

Implements Unix-style glob matching without importing fnmatch or glob.

Usage:
    python glob_match.py "*.py" "hello.py"
    python glob_match.py "src/**/*.js" "src/lib/util.js"
    python glob_match.py --test
"""

import sys


def glob_match(pattern: str, text: str, sep: str = "/") -> bool:
    """Match text against glob pattern."""
    return _match(pattern, 0, text, 0, sep)


def _match(pat: str, pi: int, txt: str, ti: int, sep: str) -> bool:
    while pi < len(pat) or ti < len(txt):
        if pi >= len(pat):
            return False

        c = pat[pi]

        # ** matches any path segments
        if c == '*' and pi + 1 < len(pat) and pat[pi + 1] == '*':
            # Skip extra *s
            while pi + 2 < len(pat) and pat[pi + 2] == '*':
                pi += 1
            # Skip trailing separator after **
            npi = pi + 2
            if npi < len(pat) and pat[npi] == sep:
                npi += 1
            # Try matching ** against 0 or more path segments
            for i in range(ti, len(txt) + 1):
                if _match(pat, npi, txt, i, sep):
                    return True
            return False

        # * matches anything except separator
        if c == '*':
            # Skip consecutive *s
            while pi + 1 < len(pat) and pat[pi + 1] == '*' and (pi + 2 >= len(pat) or pat[pi + 2] != '*'):
                pi += 1
            pi += 1
            for i in range(ti, len(txt) + 1):
                if i > ti and txt[i - 1] == sep:
                    break
                if _match(pat, pi, txt, i, sep):
                    return True
            return False

        # ? matches any single char except separator
        if c == '?':
            if ti >= len(txt) or txt[ti] == sep:
                return False
            pi += 1; ti += 1; continue

        # [...] character class
        if c == '[':
            if ti >= len(txt):
                return False
            end = pat.index(']', pi + 1)
            chars = pat[pi + 1:end]
            negate = False
            if chars.startswith('!') or chars.startswith('^'):
                negate = True
                chars = chars[1:]
            matched = False
            i = 0
            while i < len(chars):
                if i + 2 < len(chars) and chars[i + 1] == '-':
                    if chars[i] <= txt[ti] <= chars[i + 2]:
                        matched = True
                    i += 3
                else:
                    if chars[i] == txt[ti]:
                        matched = True
                    i += 1
            if negate:
                matched = not matched
            if not matched:
                return False
            pi = end + 1; ti += 1; continue

        # {a,b,c} alternation
        if c == '{':
            end = pat.index('}', pi + 1)
            alternatives = pat[pi + 1:end].split(',')
            rest = pat[end + 1:]
            return any(_match(alt + rest, 0, txt, ti, sep) for alt in alternatives)

        # Literal match
        if ti >= len(txt) or c != txt[ti]:
            return False
        pi += 1; ti += 1

    return pi >= len(pat) and ti >= len(txt)


def filter_paths(pattern: str, paths: list) -> list:
    """Return paths matching the glob pattern."""
    return [p for p in paths if glob_match(pattern, p)]


def test():
    print("=== Glob Matcher Tests ===\n")

    # Basic *
    assert glob_match("*.py", "hello.py")
    assert not glob_match("*.py", "hello.js")
    assert glob_match("hello.*", "hello.world")
    assert not glob_match("*.py", "dir/hello.py")  # * doesn't cross /
    print("✓ Wildcard *")

    # ?
    assert glob_match("?.py", "a.py")
    assert not glob_match("?.py", "ab.py")
    print("✓ Single char ?")

    # Character classes
    assert glob_match("[abc].txt", "a.txt")
    assert not glob_match("[abc].txt", "d.txt")
    assert glob_match("[!abc].txt", "d.txt")
    assert not glob_match("[!abc].txt", "a.txt")
    assert glob_match("[a-z].txt", "m.txt")
    print("✓ Character classes [...]")

    # **
    assert glob_match("**/*.py", "src/lib/hello.py")
    assert glob_match("**/*.py", "hello.py")
    assert glob_match("src/**", "src/a/b/c")
    print("✓ Globstar **")

    # {alternatives}
    assert glob_match("*.{py,js}", "hello.py")
    assert glob_match("*.{py,js}", "hello.js")
    assert not glob_match("*.{py,js}", "hello.rb")
    print("✓ Alternation {a,b}")

    # Complex patterns
    assert glob_match("src/**/test_*.py", "src/lib/test_foo.py")
    assert glob_match("src/**/test_*.py", "src/test_bar.py")
    assert not glob_match("src/**/test_*.py", "lib/test_bar.py")
    print("✓ Complex patterns")

    # Filter
    paths = ["main.py", "lib/util.py", "lib/test_util.py", "README.md", "src/app.js"]
    result = filter_paths("**/*.py", paths)
    assert len(result) == 3
    print(f"✓ Filter: {result}")

    # Edge cases
    assert glob_match("", "")
    assert not glob_match("", "a")
    assert glob_match("*", "anything")
    assert not glob_match("*", "a/b")
    print("✓ Edge cases")

    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--test":
        test()
    elif len(args) == 2:
        match = glob_match(args[0], args[1])
        print(f"{'MATCH' if match else 'NO MATCH'}: {args[0]} vs {args[1]}")
