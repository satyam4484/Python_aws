from pathlib import Path
import os
import boto3

s3cli = boto3.client('s3')
bucket = os.environ['bucket']
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
        s3cli.upload_file(os.path.join(output_dir, f"processed_{filename}"),bucket,os.path.join(output_dir, f"processed_{filename}"))

def process_files(input_dir, output_dir):
    """Main function to process input files and write to output files."""
    file_contents = read_files(input_dir)
    manipulated_contents = manipulate_content(file_contents)
    write_files(output_dir, manipulated_contents)

def make_directories():
    os.makedirs('/tmp/data_files',exist_ok=True)
    os.makedirs('/tmp/data_files/input',exist_ok=True)
    os.makedirs('/tmp/data_files/output',exist_ok=True)

def lambda_handler(event,context):
    parent_dir = Path(os.path.dirname(__file__)).parent.parent.parent
    tmp_dir = os.path.join(parent_dir,'tmp')
    
    print(tmp_dir)
    input_directory = os.path.join(data_dir,"input")
    output_directory = tmp_dir
    process_files(input_directory, '/tmp/data_files/output')

    return {'status':200,'message':'hello from python'}


# aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
