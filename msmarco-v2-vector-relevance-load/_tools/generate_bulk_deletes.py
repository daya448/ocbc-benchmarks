import json
import sys
import os

def process_ndjson(input_file, output_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    line_count = 0
    
    # Open the input and output files
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Loop through each line in the NDJSON file
        for line in infile:
            # Increment the line counter
            line_count += 1
            
            # Parse the JSON string to a dictionary
            doc = json.loads(line.strip())
            
            # Create the Elasticsearch bulk delete request dictionary
            bulk_request = {
                "delete": {
                    "_id": doc.get('docid'),  # Set the _id field from 'docid' key,
                    "_index": "vdb910-msmarco-v2"
                }
            }
            
            # Write the bulk delete request directly to the output file
            json.dump(bulk_request, outfile)
            outfile.write('\n')
            
            # Print status every 100,000 lines
            if line_count % 100000 == 0:
                print(f"Processed {line_count} lines...")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder>")
        sys.exit(1)
    
    folder = sys.argv[1]
    input_file = os.path.join(folder, 'msmarco-v2-initial-indexing', 'cohere-documents-01.json')
    output_file = os.path.join(folder, 'msmarco-v2-bulk-delete', 'cohere-deletes-01.json')
    
    process_ndjson(input_file, output_file)
    
    # Calculate the size of the output file
    output_file_size = os.path.getsize(output_file)
    
    # Print the output file size in bytes
    print(f"Processed {input_file} and output to {output_file}")
    print(f"Output file size: {output_file_size} bytes")
    
    # Instruction for adding to ESRally corpora
    print("\nTo add this file to the Elasticsearch Rally corpora, use the following steps:")
    print("1. Move the file to the appropriate location in your ESRally setup.")
    print("2. Update your ESRally track configuration to include this file.")
    print(f"3. Make sure the file path in your track configuration points to: {output_file}")

if __name__ == "__main__":
    main()
