import os
import json
import sys

def get_file_size(file_path):
    return os.path.getsize(file_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_corpora_json.py DIR")
        sys.exit(1)

    DIR = sys.argv[1]
    corpora = []

    for folder in os.listdir(DIR):
        if folder.startswith("msmarco-memory-"):
            i = int(folder.split("-")[-1])
            corpus = {
                "name": "cohere-initial-indexing",
                "base-url": "{{_base_url}}"
            }
            documents = []

            folder_path = os.path.join(DIR, folder)
            for file in os.listdir(folder_path):
                if file.endswith(".json.bz2"):
                    file_path = os.path.join(folder_path, file)
                    json_file_path = file_path[:-4]  # Remove .bz2 extension

                    document = {
                        "source-file": file,
                        "document-count": 1000000,
                        "compressed-bytes": get_file_size(file_path),
                        "uncompressed-bytes": get_file_size(json_file_path)
                    }

                    documents.append(document)

            corpus["documents"] = documents
            corpora.append(corpus)

    print(json.dumps(corpora, indent=4))

if __name__ == "__main__":
    main()
