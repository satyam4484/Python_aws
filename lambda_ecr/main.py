from pathlib import Path
import os
import boto3

s3cli = boto3.client('s3')
bucket = os.environ['bucket']
data_dir = os.path.join(os.path.dirname(__file__), 'data_files')

def read_files(input_dir):
    """Reads all text files from the input directory."""
    print(f"[DEBUG] Reading files from {input_dir}...")
    file_contents = {}

    try:
        for filename in os.listdir(input_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_dir, filename)
                with open(file_path, 'r') as file:
                    file_contents[filename] = file.readlines()
                print(f"[DEBUG] Successfully read {filename}")
        print(f"[DEBUG] Read {len(file_contents)} files in total.")
    except Exception as e:
        print(f"[ERROR] Failed to read files: {e}")
    return file_contents

def manipulate_content(file_contents):
    """Converts text to uppercase, appends a line number, and adds extra data."""
    print("[DEBUG] Manipulating content...")
    manipulated_contents = {}
    try:
        for filename, lines in file_contents.items():
            manipulated_lines = []
            for idx, line in enumerate(lines, 1):
                manipulated_lines.append(f"Processed {idx}: {line.strip().upper()}\n")
            manipulated_lines.append(f"\nTotal number of lines: {len(lines)}\n")
            manipulated_contents[filename] = manipulated_lines
            print(f"[DEBUG] Successfully manipulated {filename} with {len(lines)} lines")
        print("[DEBUG] Content manipulation completed.")
    except Exception as e:
        print(f"[ERROR] Failed to manipulate content: {e}")
    return manipulated_contents

def write_files(output_dir, manipulated_contents):
    """Writes manipulated content to output files."""
    print(f"[DEBUG] Writing files to {output_dir}...")
    try:
        for filename, lines in manipulated_contents.items():
            output_file_path = os.path.join(output_dir, f"processed_{filename}")
            with open(output_file_path, 'w') as file:
                file.writelines(lines)
            s3cli.upload_file(output_file_path, bucket, f"processed_{filename}")
            print(f"[DEBUG] Successfully wrote and uploaded {filename} to bucket {bucket} at {output_file_path}")
        print(f"[DEBUG] Files written and uploaded to S3 bucket {bucket}.")
    except Exception as e:
        print(f"[ERROR] Failed to write or upload files: {e}")

def process_files(input_dir, output_dir):
    """Main function to process input files and write to output files."""
    print(f"[DEBUG] Starting the file processing with input_dir: {input_dir} and output_dir: {output_dir}...")
    file_contents = read_files(input_dir)
    manipulated_contents = manipulate_content(file_contents)
    write_files(output_dir, manipulated_contents)
    print("[DEBUG] File processing completed.")

def make_directories():
    print("[DEBUG] Creating necessary directories...")
    try:
        os.makedirs('/tmp/data_files', exist_ok=True)
        os.makedirs('/tmp/data_files/input', exist_ok=True)
        os.makedirs('/tmp/data_files/output', exist_ok=True)
        print("[DEBUG] Directories created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create directories: {e}")

def lambda_handler(event,context):
    parent_dir = Path(os.path.dirname(__file__)).parent.parent.parent
    tmp_dir = os.path.join(parent_dir,'tmp')


    print(f"[DEBUG] Environment variable 'bucket': {bucket}")
    print(f"[DEBUG] data_dir: {data_dir}")
    print(f"[DEBUG] parent_dir: {parent_dir}")
    print(f"[DEBUG] tmp_dir: {tmp_dir}")

    input_directory = os.path.join(data_dir, "input")
    output_directory = '/tmp/data_files/output'
    
    make_directories()
    
    print(f"[DEBUG] Starting file processing with input_directory: {input_directory} and output_directory: {output_directory}...")
    process_files(input_directory, output_directory)

    print("[DEBUG] Lambda function execution completed.")
    return {'status': 200, 'message': 'hello from python'}