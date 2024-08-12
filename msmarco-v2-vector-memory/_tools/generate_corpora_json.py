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
    corpora = [None] * 30

    for folder in os.listdir(DIR):
        if folder.startswith("msmarco-memory-"):
            i = int(folder.split("-")[-1])
            corpus = {
                "name": "msmarco-memory-" + str(i)
            }
            documents = []

            folder_path = os.path.join(DIR, folder)
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    file_path = os.path.join(folder_path, file)

                    document = {
                        "source-file": file,
                        "document-count": 1000000,
                        "uncompressed-bytes": get_file_size(file_path)
                    }

                    documents.append(document)

            corpus["documents"] = documents
            corpora[i] = corpus

    corpora = [x for x in corpora if x is not None]
    print(json.dumps(corpora, indent=4))

if __name__ == "__main__":
    main()
