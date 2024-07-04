import os

data_dir = os.path.join(os.path.dirname(__file__), 'data_files')

def read_files(input_dir):
    """Reads all text files from the input directory."""
    file_contents = {}

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), 'r') as file:
                file_contents[filename] = file.readlines()
    return file_contents

def manipulate_content(file_contents):
    """Converts text to uppercase, appends a line number, and adds extra data."""
    manipulated_contents = {}
    for filename, lines in file_contents.items():
        manipulated_lines = []
        for idx, line in enumerate(lines, 1):
            manipulated_lines.append(f"Processed {idx}: {line.strip().upper()}\n")
        manipulated_lines.append(f"\nTotal number of lines: {len(lines)}\n")
        manipulated_contents[filename] = manipulated_lines
    return manipulated_contents

def write_files(output_dir, manipulated_contents):
    """Writes manipulated content to output files."""
    os.makedirs(output_dir, exist_ok=True)
    for filename, lines in manipulated_contents.items():
        with open(os.path.join(output_dir, f"processed_{filename}"), 'w') as file:
            file.writelines(lines)

def process_files(input_dir, output_dir):
    """Main function to process input files and write to output files."""
    file_contents = read_files(input_dir)
    manipulated_contents = manipulate_content(file_contents)
    write_files(output_dir, manipulated_contents)

def make_directories():
    os.makedirs('/tmp/data_files',exist_ok=True)
    os.makedirs('/tmp/data_files/input',exist_ok=True)
    os.makedirs('/tmp/data_files/output',exist_ok=True)
    
if __name__ == "__main__":
    input_directory = os.path.join(data_dir,"input")
    output_directory = os.path.join(data_dir,"output")
    process_files(input_directory, output_directory)