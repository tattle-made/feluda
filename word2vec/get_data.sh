# download all fasttext embeddings
wget "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.vec.gz"  
wget "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.hi.300.vec.gz"  
wget "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.gu.300.vec.gz"  

# extract 
gzip -dv cc.*.gz