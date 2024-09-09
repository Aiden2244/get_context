# directory_structure.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# this file handles the logic for printing the directory structure at the top of the context file.

import os

def write_directory_structure(directory, outfile, max_items=20, ignore_patterns=None, exclude_dirs=None):
    """Orchestrates writing the directory structure to the output file."""
    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        level = relative_root.count(os.sep)
        indent = ' ' * 4 * level
        current_dir = os.path.basename(root) or os.path.basename(directory)

        # Determine whether the current directory should be excluded
        if should_exclude_directory(relative_root, current_dir, ignore_patterns, exclude_dirs):
            write_directory_entry(outfile, current_dir, indent, excluded=True)
            dirs[:] = []  # Prevent os.walk from traversing excluded directories
            continue

        # Write the directory entry
        write_directory_entry(outfile, current_dir, indent, excluded=False)

        # Display subdirectories and files
        sub_indent = ' ' * 4 * (level + 1)
        items = dirs + files
        limited_items = limit_display_items(items, max_items)

        for item in limited_items:
            item_path = os.path.join(root, item)
            relative_item_path = os.path.relpath(item_path, directory)

            if os.path.isdir(item_path):
                # Check if the subdirectory should be excluded
                if should_exclude_directory(relative_item_path, item, ignore_patterns, exclude_dirs):
                    write_directory_entry(outfile, item, sub_indent, excluded=True)
                    dirs.remove(item)
                else:
                    write_directory_entry(outfile, item, sub_indent, excluded=False)
            else:
                write_directory_entry(outfile, item, sub_indent, excluded=False)

    outfile.write("\n\n" + "=" * 50 + "\n\n")


def should_exclude_directory(relative_path, directory_name, ignore_patterns, exclude_dirs):
    """Determine whether a directory should be excluded based on ignore patterns or default exclusions."""
    if ignore_patterns and ignore_patterns.match_file(relative_path):
        return True
    if exclude_dirs and directory_name in exclude_dirs:
        return True
    return False


def write_directory_entry(outfile, entry_name, indent, excluded=False):
    """Write a directory or file entry to the output file."""
    if excluded:
        outfile.write(f"{indent}{entry_name}/ (contents omitted)\n")
    else:
        outfile.write(f"{indent}{entry_name}/\n")


def limit_display_items(items, max_items):
    """Limit the number of displayed items in a directory."""
    if len(items) > max_items:
        return items[:max_items] + [f"... (truncated {len(items) - max_items} more items)"]
    return items
