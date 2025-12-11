#!/usr/bin/env python3
"""
Generate boilerplate for a new Advent of Code day.

Usage:
    python3 generate-day.py <day_number> "<title>"

Example:
    python3 generate-day.py 3 "Lobby Test"

This will create:
    03-lobby-test/
    ├── 03-lobby-test.md
    ├── 03-lobby-test.py
    ├── 03-lobby-test-part2.py
    ├── input.txt
    ├── example-input.txt
    └── attempts.txt
"""

import argparse
import os
import sys


def slugify(title: str) -> str:
    """Convert title to lowercase-hyphenated format."""
    return title.lower().replace(" ", "-")


def create_day_boilerplate(day: int, title: str):
    """Create the folder structure and files for a new day."""
    # Format day number with leading zero
    day_str = f"{day:02d}"
    slug = slugify(title)
    folder_name = f"{day_str}-{slug}"

    # Get the script directory (where this script is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, folder_name)

    # Check if folder already exists
    if os.path.exists(folder_path):
        print(f"Error: Folder '{folder_name}' already exists!")
        sys.exit(1)

    # Create the folder
    os.makedirs(folder_path)
    print(f"Created folder: {folder_name}/")

    # Create the markdown file
    md_content = f"""# Day {day}: {title} ---

[Problem description goes here]

## Part Two

[Part 2 description goes here]
"""
    md_path = os.path.join(folder_path, f"{folder_name}.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"  Created: {folder_name}.md")

    # Python boilerplate template
    python_template = """def main(content: str):
    # TODO: Implement solution
    pass

if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        raw_content = file.read()
    main(raw_content.strip())
"""

    # Create the main Python file
    py_path = os.path.join(folder_path, f"{folder_name}.py")
    with open(py_path, "w") as f:
        f.write(python_template)
    print(f"  Created: {folder_name}.py")

    # Create the part 2 Python file
    py_part2_path = os.path.join(folder_path, f"{folder_name}-part2.py")
    with open(py_part2_path, "w") as f:
        f.write(python_template)
    print(f"  Created: {folder_name}-part2.py")

    # Create empty input files
    input_path = os.path.join(folder_path, "input.txt")
    with open(input_path, "w") as f:
        f.write("")
    print("  Created: input.txt")

    example_input_path = os.path.join(folder_path, "example-input.txt")
    with open(example_input_path, "w") as f:
        f.write("")
    print("  Created: example-input.txt")

    # Create attempts file
    attempts_path = os.path.join(folder_path, "attempts.txt")
    with open(attempts_path, "w") as f:
        f.write("")
    print("  Created: attempts.txt")

    print(f"\n✅ Day {day} '{title}' boilerplate created successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate for a new Advent of Code day"
    )
    parser.add_argument("day", type=int, help="Day number (e.g., 3)")
    parser.add_argument("title", type=str, help='Day title (e.g., "Lobby Test")')

    args = parser.parse_args()

    if args.day < 1 or args.day > 25:
        print("Error: Day must be between 1 and 25")
        sys.exit(1)

    create_day_boilerplate(args.day, args.title)


if __name__ == "__main__":
    main()
