from concurrent.futures import process
import pickle
import argparse
import os, os.path
from datetime import datetime

def verify_documents_dir(arg):
    if os.path.isdir(arg):
        return arg
    error_mssg = "The directory does not exist."
    raise argparse.ArgumentTypeError(error_mssg)
    
def process_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("documents_dir", type=verify_documents_dir, help="The directory containing the documents and metadata")
    parser.add_argument("find_type", choices=['docno', 'id'], help="Type of id to look for document")
    parser.add_argument("id", help="Docno or docid to search document by")
    return parser.parse_args()

def build_output(doc):
    metadata = ""
    metadata += f"docno: {doc.docno}\n"
    metadata += f"internal id: {doc.docid}\n"
    datetime_str = f"{doc.month}/{doc.date}/{doc.year}"
    datetime_obj = datetime.strptime(datetime_str, '%m/%d/%y')
    metadata += f"date: {datetime_obj.strftime('%B %d, %Y')}\n"
    metadata += f"headline: {doc.headline.strip()}\n"
    raw = "raw document:\n"
    with open(doc.rawFilePath, 'r') as f:
        raw += f.read()
    return metadata + raw

def main():
    args = process_argument()
    with open(f'{args.documents_dir}/metadata.pkl', 'rb') as handle:
        doc_map = pickle.load(handle)
    
    id_doc = doc_map[0]
    docno_id = doc_map[2]

    # find doc by id 
    if args.find_type == "docno":
        id = docno_id[args.id]
        if not id:
            print("Document does not exist")
            return
        doc = id_doc[id]
        
    if args.find_type == "id":
        if args.id not in id_doc.keys():
            print("Document does not exist")
            return
        doc = id_doc[args.id]
        
    print(build_output(doc))
    
    
if __name__ == "__main__":
    main()