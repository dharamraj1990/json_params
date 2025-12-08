#!/usr/bin/env python3
"""
Simple script that loads environment variables from env.DEV file and prints them.
Works with python-dotenv if installed; otherwise uses a small parser.

Usage:
  python3 script.py /path/to/env.DEV

If you want it to load into os.environ as well, it will.
"""
import os
import sys
from pathlib import Path

def load_dotenv_simple(path: Path):
    """Lightweight parser for .env file: KEY=VALUE, ignores comments and blank lines."""
    env = {}
    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            env[key] = val
    return env

def main():
    if len(sys.argv) > 1:
        env_path = Path(sys.argv[1])
    else:
        env_path = Path('env.DEV')

    if not env_path.exists():
        print(f"ERROR: env file not found: {env_path}", file=sys.stderr)
        sys.exit(2)

    # try to use python-dotenv if available
    try:
        from dotenv import dotenv_values
        env = dotenv_values(env_path)
        # dotenv_values returns dict with None for unparsable lines - filter them
        env = {k: v for k, v in env.items() if k}
    except Exception:
        env = load_dotenv_simple(env_path)

    # Optionally inject into os.environ (uncomment if needed)
    # os.environ.update({k: str(v) for k, v in env.items()})

    # Print everything
    print(f"Loaded {len(env)} keys from {env_path}:")
    for k in sorted(env.keys()):
        print(f"{k}={env[k]}")

    # Example: print a specific variable if present
    # For demonstration print a known key
    # print("MY_VAR:", env.get("MY_VAR"))

if __name__ == "__main__":
    main()
