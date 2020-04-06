import re
import os
import time
import random
import datetime
from wiki_dump_parser import Cleaner, iterate
from nltk.tokenize import sent_tokenize

def clean_title(title):
    no_space = title.replace(' ', '_')
    no_dash = no_space.replace('-', '_')
    return re.sub(r'\W+', '', no_dash) + '_' + str(random.randint(10,99))

src = input('input file name: ')
dest = input('output file name: ')

i = 0
err = 0
start_time = datetime.datetime.now()
dest = open(dest, 'w')

cleaner = Cleaner()

for title, text in iterate(raw_dump):
    if title is None:
        continue
    cleaned_title = clean_title(title)

    text = cleaner.clean_text(text)
    cleaned_text, links = cleaner.build_links(text)
        
    sentences = sent_tokenize(cleaned_text)
    identified_sentences = []
    j = 1
    for sentence in sentences:
        sentence = sentence.replace('\t', ' ').strip()
        sentence = re.sub(r' \(.*\)', '', sentence)
        if '==' in sentence and '\n' in sentence:
            sentence = sentence.split('\n')[-1]
        if '==' in sentence and len(sentence) < 50:
            continue
        if '{|' in sentence:
            continue
        if '\n' in sentence:
            for sentence in sentence.split('\n'):
                if len(sentence) > 100:
                    identified_sentences.append('{}-{}\t{}'.format(cleaned_title, j, sentence))
                    j += 1
            continue
        identified_sentences.append('{}-{}\t{}'.format(cleaned_title, j, sentence))
        j += 1
    try:
        dest.write('\n'.join(identified_sentences) + '\n')
    except:
        err += 1
    i += 1
    if i % 1000 == 0:
        print(
            '\rpages processed: {} | error: {} | elapsed: {}'.format(
                i, err, str(datetime.datetime.now() - start_time).split('.')[0]
            ), sep=' ', end='', flush=True
        )

print('script finished at', datetime.datetime.now())
