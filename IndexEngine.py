import argparse
from genericpath import isdir, isfile
import gzip
import os, os.path
import re
import pickle
from document import Document


ALL_TAGS = {"<DOC>", "</DOC>", "<DOCNO>", "</DOCNO>", "<DOCID>", "</DOCID>", "<HEADLINE>", "</HEADLINE>"}


def verify_datapath(arg):
    if os.path.isfile(arg):
        return arg
    
    error_message = f"The data filepath [{arg}] does not exist."
    if os.path.isdir(arg):
        error_message = "The data filepath must be a file."
    
    raise argparse.ArgumentTypeError(error_message)


def verify_output_dir(arg):
    if os.path.isdir(arg):
        error_message = "The directory already exists."
        raise argparse.ArgumentTypeError(error_message)
    return arg


def is_closing_tag(tag):
    return True if tag[1] == '/' else False

       
def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


def process_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_filepath", type=verify_datapath, help="The original data file path")
    parser.add_argument("output_dir", type=verify_output_dir, help="The output directory for the documents")
    return parser.parse_args()


def process_input_datafile(input_filepath):
    with gzip.open(input_filepath, 'rt') as f:
        file_content = f.read()
    return file_content


def process_documents(file_content, output_dir):
    # return a list of Document objects and write documents into files
    id_doc = {}
    id_docno = {}
    docno_id = {}
    # find list of tags
    pattern = r"<\/?[A-Z]+>"
    tags = re.finditer(pattern, file_content)
    
    tag_stack = []
    cur_doc = Document()
    for tag in tags:
        if tag[0] not in ALL_TAGS:
            continue
        if not is_closing_tag(tag[0]):
            tag_stack.append(tag)
        else:
            if not tag_stack:
                print(tag)
            open_tag = tag_stack.pop()
            if tag[0] == "</DOCNO>":
                cur_doc.docno = file_content[open_tag.end() + 1: tag.start() - 1]
                cur_doc.month = cur_doc.docno[2:4]
                cur_doc.date = cur_doc.docno[4:6]
                cur_doc.year = cur_doc.docno[6:8]
            if tag[0] == "</DOCID>":
                cur_doc.docid = file_content[open_tag.end() + 1: tag.start() - 1]
            if tag[0] == "</HEADLINE>":
                cur_doc.headline = re.sub(r"<\/?[P]+>", "", file_content[open_tag.end() + 1: tag.start() - 1])
            if tag[0] == "</DOC>":
                # create raw file
                raw_doc = file_content[open_tag.start() : tag.end()]
                cur_doc.rawDoc = raw_doc
                raw_file_path = f'{output_dir}/{cur_doc.year}/{cur_doc.month}/{cur_doc.date}/{cur_doc.docno}'
                cur_doc.rawFilePath = raw_file_path
                with safe_open_w(raw_file_path) as f:
                    f.write(raw_doc)
                
                # map docid with doc object 
                id_doc[cur_doc.docid] = cur_doc
                id_docno[cur_doc.docid] = cur_doc.docno
                docno_id[cur_doc.docno] = cur_doc.docid
                cur_doc = Document()
    
    return [id_doc, id_docno, docno_id]


def write_metadata_file(dicts, output_dir):
    # Get a list of document objects, write into a metadata file
    with open(f'{output_dir}/metadata.pkl', 'wb') as handle:
        pickle.dump(dicts, handle, protocol = pickle.HIGHEST_PROTOCOL)
    
    
def main():
    args = process_argument()
    file_content = process_input_datafile(args.data_filepath)
    dicts = process_documents(file_content, args.output_dir)
    write_metadata_file(dicts, args.output_dir)
        

if __name__ == "__main__":
    main()