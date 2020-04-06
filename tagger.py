import datetime
import time
import random
import sys
from codes.corpus import Corpus
from codes.lexicon import Lexicon
from codes.hypernymy import pos_tag

lexicon = Lexicon()
corpus = Corpus(lexicon, src='wikicorpus_clean.tsv')

NUM_WORKERS = int(sys.argv[1])
WORKER_ID = int(sys.argv[2])

OUTPUT = 'wikicorpus_postagged_{}.tsv'.format(WORKER_ID)
TAGGER_DIR = 'taggers/tagger{}/tagger'.format(WORKER_ID)

print('output:', OUTPUT)
print('tagger:', TAGGER_DIR)

start_time = datetime.datetime.now()

BATCH_SIZE = 50

with open(OUTPUT, 'w') as f:
    count = 0
    err_count = 0
    batch_ids = []
    batch_input = ''
    
    def batch_problem(tagged):
        print('batch:')
        for b in batch_ids:
            print(b, end=' ')
        print('\ntagged:')
        for t in tagged:
            print(t)
        print('------------------')
        print('batch input:', batch_input)
        print('------------------')

    def process_batch():
        try:
            tagged = pos_tag(batch_input, tagger_dir=TAGGER_DIR).split('——/X')
        except:
            batch_problem([])
            return 1
        out = ''
        for i, entry_id in enumerate(batch_ids):
            if i < len(tagged):
                out += entry_id + '\t' + tagged[i] + '\n'
            else:
                print('problem in this entry: ', entry_id)
                batch_problem(tagged)
                break
        f.write(out)
        if count % (BATCH_SIZE * 5) == 0:
            print('processed entries: {} | elapsed: {} | errors: {}'.format(
                count, str(datetime.datetime.now() - start_time).split('.')[0], err_count
            ), flush=True)
        return 0
    for i, e in enumerate(corpus.get_all_entries()):
        if i % NUM_WORKERS != WORKER_ID:
            continue
        count += 1
        title, sentence_id = e.get_id().split(': ')
        batch_ids.append(title.replace(' ', '_') + '_' + str(random.randint(0, 100)) + '-' + sentence_id)
        batch_input += e.get_sentence() + ' —— '
        if count % BATCH_SIZE == 0:
            err_count += process_batch()
            batch_ids = []
            batch_input = ''
    if len(batch_input) > 0:
        process_batch()

print('done')