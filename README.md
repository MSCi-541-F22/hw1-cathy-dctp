# MSCI-541-HW1

Name: Duong Cat Tuong (Cathy) Pham

Description: 

### IndexEngine.py
- Used to read the latimes.gz file and store separately each document and its associated metadata
- Accepts two command line arguments: a path to the latimes.gz file and a path to a directory where the documents and metadata will be stored 
- The directory where the documents and metadata are stored must not already exist 

    `/usr/bin/python3 "/Users/cathyp/Documents/fall 2022/541/hw1-cathy-dctp/IndexEngine.py" latimes.gz output`

### GetDoc.py
- Used to retrieve a document and its metadata
- Accepts three command line arguments: a path to the location of the documents and metadata store, find_type ("id" or "docno"), and either the integer id or a document or a DOCNO, depending on the specified find_type 

    `/usr/bin/python3 "/Users/cathyp/Documents/fall 2022/541/hw1-cathy-dctp/GetDoc.py" output docno LA010189-0018`

