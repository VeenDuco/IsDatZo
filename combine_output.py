import os

__OUTPUT_DIR = 'output_pdf'

def combine_files_for_combination(base_file_name, topic):
    """
    Combine all files for a given document-topic combination into a single file.
    """
    combined_content = ""
    idx = 0

    # Construct the filename pattern for the combination
    filename_pattern = f"{base_file_name}-{topic}-"

    # Loop until we don't find a file matching the pattern
    while True:
        current_file = os.path.join(__OUTPUT_DIR, f"{filename_pattern}{idx:04d}.txt")
        if os.path.exists(current_file):
            try:
                with open(current_file, 'r', encoding='utf-8') as f:
                    combined_content += f.read() + "\n\n"  # Add content and two newlines for separation
            except UnicodeDecodeError:
                # If there's an encoding error with utf-8, try reading with 'utf-8-sig' or 'ISO-8859-1'
                try:
                    with open(current_file, 'r', encoding='utf-8-sig') as f:
                        combined_content += f.read() + "\n\n"
                except:
                    with open(current_file, 'r', encoding='ISO-8859-1') as f:
                        combined_content += f.read() + "\n\n"
            idx += 1
        else:
            break

    # Write the combined content to a new file
    combined_filename = os.path.join(__OUTPUT_DIR, f"{base_file_name}-{topic}-combined.txt")
    with open(combined_filename, 'w', encoding='utf-8') as f:
        f.write(combined_content)

    print(f"Combined content for {base_file_name}-{topic} written to {combined_filename}")


def main():
    # Get a list of all files in the output directory
    all_files = os.listdir(__OUTPUT_DIR)

    # Extract unique combinations of document and topic from filenames
    combinations = set()
    for filename in all_files:
        if filename.endswith("-combined.txt"):
            continue  # Skip already combined files
        parts = filename.split('-')
        if len(parts) > 2:  # Ensure filename has the expected format
            base_file_name = parts[0]
            topic = parts[1]
            combinations.add((base_file_name, topic))

    # Combine files for each unique combination
    for base_file_name, topic in combinations:
        combine_files_for_combination(base_file_name, topic)


if __name__ == "__main__":
    main()
