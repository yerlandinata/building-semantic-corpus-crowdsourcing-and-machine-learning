# Introduction
The codes here was rewritten from working codes, but not tested again, so copy paste may not work.

Codes are written for Ubuntu OS.

- Yudhistira Erlandinata

# Dependencies
You may need some privilleges
```
git clone https://github.com/yerlandinata/tacodes.git codes
pip install nltk 
apt install foma-bin
```

# 1. Raw Wikipedia Dump Cleaning
Clean the wikipedia dump from unreadable unicode characters.

### Input
Download this file from Wikimedia Dump: `idwiki-latest-pages-articles.xml`

### Output
The input file format does not change

# 2. Wikipedia Sentence Corpus
Create sentence corpus from wikipedia dump

### Input
Cleaned `idwiki-latest-pages-articles.xml`

### Output
Sentence corpus in TSV format. The columns are: 
- Wikipedia page title (uniqueness guaranteed)
- Sentence number of current wikipedia page
- Sentence

# 3. Sentence Corpus Cleaning
Filter out invalid tokens. Punctuations are considered valid tokens. Example of invalid token: `!@##$~n0t3v3n4w0rd___++`

### Input
Wikipedia Sentence Corpus (tsv)

### Output
The input file format does not change

# 4. POS Tagging
This is kind of tricky because we want to utilize all CPU cores and all available system memory.

For each CPU cores, we can have 1 tagger process. For each tagger process, it use up to 4GB of system memory.

### Input
Wikipedia Sentence Corpus (tsv)

### Output
The input file format does not change

### Step by step guide
- Download Indonesian Postagger from here: https://github.com/andryluthfi/indonesian-postag 
- Download **latest** MorphInd from here: https://septinalarasati.com/morphind/
- Create `taggers` directory, and then inside of this dir, create taggerN directory for each tagger process.
- Each taggerN directory must have 2 directories: `tagger` (copy of Indonesian Postagger) and `morphind` (copy of MorphInd)
- Input file is `wikicorpus_clean.tsv`
- Run `bash 4_postag.sh {number of process}` (On Intel Core i7-5960X 16 core 32 thread and 64GB memory, you can use 16 process, and the job will take 6-7 hours)
- Output files: `wikicorpus_postagged_N.tsv` for each tagger process
- Aggregate all `wikicorpus_postagged_N.tsv` into one tsv

# 5. Convert Foreign Words and Unknown POS Tags to be Nouns
Optional step and can be skipped.

### Input
Wikipedia Sentence Corpus (tsv)

### Output
The input file format does not change

# 6. Pattern Matching
Uses patterns defined in patterns dir and do the pattern matching.

### Input
- pattern: take example in patterns dir
- Wikipedia Sentence Corpus (tsv)

### Output
JSON

