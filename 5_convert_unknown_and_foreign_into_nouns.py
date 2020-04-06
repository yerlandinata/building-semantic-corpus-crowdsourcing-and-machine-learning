import string
from codes.corpus import Corpus
from codes.lexicon import Lexicon

lexicon = Lexicon()
corpus = Corpus(lexicon, src=input('input file: '))

enriched_set = set()

def enrich_nouns(tagged_tokenized):
    count = 0
    result = []
    for token in tagged_tokenized:
        try:
            word, tag = token.split('/')
        except ValueError:
            continue
        clean = word.lower()
        if len(clean) == 0:
            continue
        if clean[-1] in string.punctuation:
            clean = clean[::-1]
        if clean[0] in string.punctuation:
            clean = clean[1:]
        if tag == 'X' or tag == 'FW':
            try:
                lexicon_entry = lexicon.get_entry(clean)
                if lexicon_entry.pos == 'Nomina':
                    enriched_set.add(clean)
                    result.append(word + '/' + 'NN')
                    count += 1
                    continue
            except KeyError:
                pass
        result.append(token)
    return result, count

count_enriched = 0
with open(input('output file: '), 'w') as f:
    for i, e in enumerate(corpus.get_all_entries()):
        enriched, count = enrich_nouns(e.get_postag_tokenized())
        f.write('{}\t{}\n'.format(e.get_original_identifier(), ' '.join(enriched)))
        count_enriched += count
        if i % 100000 == 0:
            print('\rProcessed:', i, 'Enriched:', count_enriched, end='', flush=True)
            