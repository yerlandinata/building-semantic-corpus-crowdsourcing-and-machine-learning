import json
import datetime
import time
from codes.pattern_matcher import PatternMatcher
from codes.corpus import Corpus
from codes.lexicon import Lexicon

lexicon = Lexicon()
corpus = Corpus(lexicon, src=input('input sentence corpus tsv file: '))
out = input('output file name (JSON): ')
pattern_matcher = PatternMatcher('patterns/made_2017_modified.txt')

pairs = dict()
start_time = datetime.datetime.now()

for i, e in enumerate(corpus.get_all_entries()):
    sentence = ' '.join(list(map(lambda t: t.replace(' ', '_'), e.get_postag_tokenized())))
    w1, w2, pattern = pattern_matcher.match(sentence)
    if w1 is not None:
        if (w1, w2) not in pairs:
            pairs[(w1, w2)] = []
        pairs[(w1, w2)].append(pattern)
    if i % 100000 == 0:
        print('\rprocessed entries: {} | unique collected pairs: {} | elapsed: {}'.format(
            i, len(pairs.keys()), str(datetime.datetime.now() - start_time).split('.')[0]
        ), end='', flush=True)        
    
        
with open(out, 'w') as f:
    json.dump({str(p): pairs[p] for p in pairs.keys()}, f)
