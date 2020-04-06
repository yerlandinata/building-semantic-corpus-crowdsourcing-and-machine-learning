import datetime
from nltk.tokenize import word_tokenize
from codes.cleaner import is_valid_word
from codes.utils import pipe

src = open(input('input file: '), 'r')
dest = open(input('output file: '), 'w')

start_time = datetime.datetime.now()
i = 0

while True:
    line = src.readline()
    if line == '':
        break
    identifier, sentence = line.split('\t')
    if 'ALIH' in sentence:
        continue
    tokenized = word_tokenize(sentence)
    sentence = ' '.join(list(filter(is_valid_word, tokenized)))
    sentence = sentence.replace('/', ' / ').replace('  ', ' ')
    dest.write(identifier + '\t' + sentence.strip() + '\n')
    i += 1
    if i % 25000 == 0:
        print('\rprocessed entries: {} | elapsed: {}'.format(
            i, str(datetime.datetime.now() - start_time).split('.')[0]
        ), end='', flush=True)
    
src.close()
dest.close()
