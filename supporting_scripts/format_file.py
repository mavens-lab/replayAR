import argparse

def rearrange_and_format_file(input_path, output_path):
    # Open the input file for reading and the output file for writing
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            # Skip comments or empty lines
            if line.startswith('#') or not line.strip():
                continue
            
            line = line.replace(',', ' ').strip()
            
            # Split the line into components based on spaces
            parts = line.split()
            
            # Rearrange qw to the end
            # The index of qw is assumed to be 4
            q_RS_w = parts.pop(4)
            parts.append(q_RS_w)
            
            # Join the parts back into a single string with spaces
            formatted_line = ' '.join(parts) + '\n'
            
            outfile.write(formatted_line)

if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='This script reformats a trace from timestamp tx ty tz qw qx qy qz to timestamp tx ty tz qx qy qz qw.')
    parser.add_argument('first_file', help='output file(format: timestamp tx ty tz qx qy qz qw)')
    parser.add_argument('second_file', help='output file (format: timestamp tx ty tz qx qy qz qw)')

    args = parser.parse_args()

    rearrange_and_format_file(args.first_file, args.second_file)
    # Example usage
    '''input_file_path =  "Case3Tests/updated_version/trace_4/f_hololens2-dataset-MH04_stereo.txt"
    output_file_path = "Case3Tests/updated_version/trace_4/Orbslam_Trace4_Formatted.txt"
    rearrange_and_format_file(input_file_path, output_file_path)'''
