import os
import argparse
import pyperclip
import sys
import io

def print_tree(directory, prefix=''):
    output = []
    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if not e.startswith('.')]  # Ignore hidden files
    
    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        connector = '└── ' if index == len(entries) - 1 else '├── '
        output.append(prefix + connector + entry)
        if os.path.isdir(path):
            extension = '    ' if index == len(entries) - 1 else '│   '
            output.extend(print_tree(path, prefix + extension))
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display a directory and file tree.")
    parser.add_argument("directory", nargs="?", default=os.getcwd(),
                        help="Path to the directory to display. Defaults to current directory.")
    parser.add_argument("-o", "--output", default="tree.txt",
                        help="Path to the UTF-8 file to save the tree. Defaults to tree.txt in current directory.")
    args = parser.parse_args()

    # Ensure stdout uses UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    if os.path.isdir(args.directory):
        parent_dir_name = os.path.basename(os.path.normpath(args.directory))
        output = [parent_dir_name]
        output.extend(print_tree(args.directory))
        result = "\n".join(output)

        # Print to console
        print(result)

        # Copy to clipboard
        pyperclip.copy(result)

        # Save to UTF-8 file
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"\n✅ Tree written to {args.output} (UTF-8 encoded)")
    else:
        print("Invalid directory path.")