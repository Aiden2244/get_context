# merger.py

# Copyright (c) Aiden R. McCormack. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for more information.

# This file handles the core functionality of the program.

import os
from .directory_structure import write_directory_structure
from .file_utils import is_human_readable, has_valid_extension
from .ignore_utils import load_ignore_patterns, get_ignored_items

def merge_files_in_directory(directory, valid_extensions=None, output_file='context.txt'):
    # Check if the output file exists, and delete it if it does
    if os.path.exists(output_file):
        os.remove(output_file)

    ignore_patterns = None
    ignore_dir = None  # Track which ignore file is being used

    # Check for .contextignore file, otherwise fall back to .gitignore or default
    if os.path.exists(".contextignore"):
        ignore_dir = ".contextignore"
        ignore_patterns = load_ignore_patterns(ignore_dir)
    elif os.path.exists(".gitignore"):
        ignore_dir = ".gitignore"
        ignore_patterns = load_ignore_patterns(ignore_dir)

    # Default directories to exclude only if no ignore file is found
    default_exclude_dirs = ['env', 'venv', '__pycache__', '.git', 'build', 'dist']

    # Use default exclusions if no ignore file is present
    if ignore_patterns is None:
        print("Using default exclusions for build-related directories:")
        exclude_dirs = default_exclude_dirs
    else:
        print(f"Using ignore patterns from {ignore_dir} for brevity:")
        exclude_dirs = []  # Don't use default exclusions when an ignore file is present
        print(get_ignored_items(ignore_dir))
    
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Write the directory structure at the top of the file
        outfile.write("Directory Structure:\n")
        write_directory_structure(directory, outfile, ignore_patterns=ignore_patterns, exclude_dirs=exclude_dirs)

        # Walk through all files and subdirectories in the provided directory
        for root, dirs, files in os.walk(directory):
            # Apply exclusion logic based on ignore patterns or default list
            if ignore_patterns:
                dirs[:] = [d for d in dirs if not ignore_patterns.match_file(os.path.join(root, d))]
            else:
                # If no ignore file, use the default exclusions
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = os.path.join(root, file)

                # Skip the output file (context.txt) itself
                if file == output_file:
                    continue

                # Skip files based on ignore patterns
                if ignore_patterns and ignore_patterns.match_file(file_path):
                    continue

                # If valid extensions are provided, only include matching files
                if valid_extensions and not has_valid_extension(file, valid_extensions):
                    continue

                # Check if the file is human-readable
                if is_human_readable(file_path):
                    try:
                        # Try to open the file and read its contents in UTF-8
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(f"{os.path.relpath(file_path, directory)}\n")
                            outfile.write(infile.read())
                            outfile.write("\n\n" + "=" * 50 + "\n\n")
                    except (UnicodeDecodeError, IOError):
                        # Handle files that cannot be read in UTF-8
                        outfile.write(f"{os.path.relpath(file_path, directory)}\n")
                        outfile.write("Text not generated, file is not human-readable or could not be decoded\n\n")
                        outfile.write("=" * 50 + "\n\n")
                else:
                    # Write a message for non-human-readable files
                    outfile.write(f"{os.path.relpath(file_path, directory)}\n")
                    outfile.write("Text not generated, file is not human-readable\n\n")
                    outfile.write("=" * 50 + "\n\n")
    
    print(f"Generated 'context.txt' at '{os.getcwd()}/context.txt'")

