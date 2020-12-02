import wget
import logging
import re
import gzip
import os
from time import perf_counter

download_links = [
"https://dl.fbaipublicfiles.com/fasttext/vectors-aligned/wiki.en.align.vec",
"https://dl.fbaipublicfiles.com/fasttext/vectors-aligned/wiki.ta.align.vec",
"https://dl.fbaipublicfiles.com/fasttext/vectors-aligned/wiki.bn.align.vec",
"https://dl.fbaipublicfiles.com/fasttext/vectors-aligned/wiki.hi.align.vec",
"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.vec.gz",
"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.hi.300.vec.gz",
"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.gu.300.vec.gz"
]

zipped_files = [
"cc.gu.300.vec.gz", 
"cc.hi.300.vec.gz", 
"cc.en.300.vec.gz"
]

def download():
    print("Downloading word vectors ...")
    start = perf_counter()
    success=0  
    for link in download_links:
        for x in range(4): # try 5 times
            try:
                print("Attempting to download {}".format(link))
                wget.download(link)
                print("Downloaded {}".format(link))
                success+=1
                break
            except Exception:
                print("Attempt {} of 5 failed. Error message below:".format(x))
                print(logging.traceback.format_exc())
                pass
    delta = (perf_counter() - start)/60
    print("Time taken to download: ", delta, " minutes")
    return success

def unzip():
    print("Unzipping word vectors ...")
    start = perf_counter()
    success=0
    pattern = r'(.*?).gz'
    for f in zipped_files:
        for x in range(4): # try 5 times
            try:
                print("Attempting to unzip {}".format(f))
                data = gzip.open(f)
                filename = re.search(pattern, f).group(1)
                with open(filename, "wb") as out:
                    for line in data:
                        out.write(line)
                print("Unzipped {}".format(f))
                success+=1
                print("Deleting zipped file")
                os.remove(f)
                break
            except Exception:
                print("Attempt {} of 5 failed. Error message below:".format(x))
                print(logging.traceback.format_exc())
                pass
    delta = (perf_counter() - start)/60
    print("Time taken to unzip: ", delta, " minutes")
    return success

def download_vecs():
    download_success = download()
    if download_success == len(download_links):
        print("Downloaded all vectors")
        unzip_success = unzip()
        if unzip_success == len(zipped_files):
            print("Unzipped all zipped files")
        else:
            print("Unzipped {} out of 3 files. Please debug and try again, or unzip manually.".format(unzip_success))
    else:
        print("Downloaded {} out of 7 files. Please debug and try again, or unzip manually.".format(download_success))


if __name__ ==  "__main__":
    download_vecs()