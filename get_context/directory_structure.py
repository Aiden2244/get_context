# directory_structure.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# this file handles the logic for printing the directory structure at the top of the context file.

import os

def write_directory_structure(directory, outfile, max_items=20, ignore_patterns=None, exclude_dirs=None):
    """Write the directory structure as plain text to the output file, omitting contents of excluded directories."""
    for root, dirs, files in os.walk(directory):
        # Determine the indentation level based on directory depth
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level

        # Get the base name of the current directory
        current_dir = os.path.basename(root) or os.path.basename(directory)

        # Check if the current directory should be excluded
        is_excluded = False
        if ignore_patterns and ignore_patterns.match_file(root):
            is_excluded = True
        elif exclude_dirs and current_dir in exclude_dirs:
            is_excluded = True

        # Write the directory name with "(contents omitted)" if excluded
        if is_excluded:
            outfile.write(f"{indent}{current_dir}/ (contents omitted)\n")
            dirs[:] = []  # Do not traverse subdirectories of this directory
            continue  # Skip to the next iteration

        else:
            outfile.write(f"{indent}{current_dir}/\n")

        # Prepare subdirectories and files for display
        sub_indent = ' ' * 4 * (level + 1)
        items = dirs + files

        # Limit the number of displayed items in each directory
        for i, item in enumerate(items):
            if i >= max_items:
                outfile.write(f"{sub_indent}... (truncated {len(items) - max_items} more items)\n")
                break

            item_path = os.path.join(root, item)
            if os.path.isdir(item_path):
                # Check if the subdirectory should be excluded
                if ignore_patterns and ignore_patterns.match_file(item_path):
                    outfile.write(f"{sub_indent}{item}/ (contents omitted)\n")
                    dirs.remove(item)  # Remove from dirs to prevent os.walk from traversing it
                elif exclude_dirs and item in exclude_dirs:
                    outfile.write(f"{sub_indent}{item}/ (contents omitted)\n")
                    dirs.remove(item)  # Remove from dirs to prevent os.walk from traversing it
                else:
                    outfile.write(f"{sub_indent}{item}/\n")
            else:
                outfile.write(f"{sub_indent}{item}\n")

    outfile.write("\n\n" + "=" * 50 + "\n\n")



