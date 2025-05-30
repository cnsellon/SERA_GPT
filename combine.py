#Sera GPT
import os
from datetime import datetime, timezone
import glob

# Base setup
base_directory = "."
output_file = os.path.join(base_directory, "SERA_GPT.txt")

# Define ordered sections and their priority files (if any)
sections = [
    ("core", ["role_objectives.txt"]),            # Roles and Objectives
    ("core", ["engagement_protocol.txt"]),        # Engagement Protocol
    ("core", ["reasoning.txt"]),                  # Reasoning
    ("context", ["session_start_checks.txt"]),    # Session checks (core)
    ("context", None),                            # Additional context (dynamic catch-all)
    ("memory_archive", None),                     # Memory Archive
    ("sandbox", None),                            # Sandbox
]

# Files to exclude from combining
exclude_files = ["README.md", "readme.md", "README.txt", "readme.txt"]

# Visual divider for file boundaries
section_divider = "═══════════════════════════════════════════════════════════════════════════════\n\n"

# Function to read and clean a file's content
def read_clean_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Function to check if file should be excluded
def is_excluded(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            return first_line.startswith("[exclude]")
    except:
        return False

# Get current UTC timestamp
current_timestamp = datetime.now(timezone.utc).strftime("%m/%d/%Y %H:%MUTC")

# Begin compiling
with open(output_file, "w", encoding="utf-8") as combined:
    # Header block
    combined.write("# GPT Session Profile\n")
    combined.write(f"**Last Updated:** {current_timestamp}\n")
    combined.write("---\n\n")

    for folder_name, priority_files in sections:
        folder_path = os.path.join(base_directory, folder_name)
        if not os.path.isdir(folder_path):
            continue

        if priority_files:
            for file_name in priority_files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and not is_excluded(file_path):
                    content = read_clean_file(file_path)
                    if content:
                        combined.write(content + "\n\n" + section_divider)
        else:
            for file_name in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, file_name)
                if (
                    file_name.lower() in exclude_files
                    or not file_name.endswith(".txt")
                    or is_excluded(file_path)
                ):
                    if is_excluded(file_path):
                        print(f"Skipping file due to [exclude] marker: {file_name}")
                    continue
                content = read_clean_file(file_path)
                if content:
                    combined.write(content + "\n\n" + section_divider)

    # Append all user_background_*.txt files
    user_profiles = sorted(glob.glob(os.path.join(base_directory, "context", "user_background_*.txt")))
    for profile_path in user_profiles:
        if is_excluded(profile_path):
            print(f"Skipping file due to [exclude] marker: {os.path.basename(profile_path)}")
            continue
        content = read_clean_file(profile_path)
        if content:
            combined.write(content + "\n\n" + section_divider)

    # Final instructions (no divider after)
    final_path = os.path.join(base_directory, "core", "final_instructions.txt")
    if os.path.isfile(final_path) and not is_excluded(final_path):
        final_content = read_clean_file(final_path)
        if final_content:
            combined.write(final_content + "\n")

print(f"✅ Combined file created successfully: {output_file}")