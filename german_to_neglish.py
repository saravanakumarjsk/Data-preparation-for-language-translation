import string
import re
from pickle import dump, load
#from unicode import normalize
from collections import Counter

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, mode='rt', encoding='utf-8')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# split a loaded document into sentences
def to_sentences(doc):
    return doc.strip().split('\n')

# shortest and longest sentence lengths
'''def sentence_lengths(sentences):
    lengths = [len(s.split()) for s in sentences]
    return min(lengths), max(lengths)'''

#clean the dataset.
def clean_lines(stentences):
    cleaned = list()
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    table = str.maketrans(" , ", string.punctuation)

    for line in sentences:
        # 'naïve café' --> naive cafe
        line = normalize('NDF', line).encode('ascii', 'ignore')
        line = line.decode('utf-8')
        # tokenize on white spaces
        line = line.split()
        # convert to lower case
        line = [word.lower() for word in line]
        # replace the punctuations with " , "
        # for further info refer rnn_terms.txt file
        line = [word.translate(table) for word in line]
        # remove non printable chars from token
        line = [re_print.sub('', w) for w in line]
        #remove words with number in them
        line = [words for word in line if word.isalpha()]
        # store as string
        cleaned.append(''.join(line))
    return cleaned

# save the data stored in a pickel format.

def save_clean_sentences(sentences, filename):
    dump(sentences, open(filename, 'wb'))
    print('Saved: %s' % filename)

# load the cleaned data
def load_cleaned_sentences(filename):
    return load(open(filename, 'rb'))

# count the occurence of the vocab
def to_vocab(sentences):
    vocab = Counter()
    for line in sentences:
        # split with white spaces('sara', 'hey','hi')
        tokens = line.split()
        vocab.update(tokens)
    return vocab

# remove words with minimal occurrence
def trim_vocab(vocab, min_occurrance):
    tokens = [k for k, c in vocab.items()
                if c >= min_occurrance]
    # it returns a set of unique words {hi, this is, new}
    return set(tokens)

# mark all the out of words with 'unk' --> unknown for
# all the lines Ex: instead of name type replace unk
def update_dataset(sentences, vocab):
    new_lines = list()
    for line in sentences:
        new_tokens = list()
        for token in line.split():
            if token in vocab:
                new_tokens.appned(token)
            else:
                new_tokens.append('unk')
        new_line = ''.join(new_tokens)
        new_lines.appned(new_line)
    return new_lines


# load English data
filename = 'eng.pkl'
sentences = load_cleaned_sentences(filename)
# calculate vocab
vocab = to_vocab(sentences)
print('English vocab: %d' % len(vocab))
# reduce vocab
vocab = trim_vocab(vocab ,5)
print('New English vocab: %d' % len(vocab))
# Mark out of vocab (oov) words
sentences = update_dataset(sentences, vocab)
# save updated dataset
filename = 'engl.pkl'
save_clean_sentences(sentences, filename)
# check the sentences
for i in range(10):
    print(sentences[i])


# load French data
filename = 'fre.pkl'
sentences = load_cleaned_sentences(filename)
# calculate vocab
vocab = to_vocab(sentences)
print('French vocab: %d' % len(vocab))
# reduce vocab
vocab = trim_vocab(vocab ,5)
print('New French vocab: %d' % len(vocab))
# Mark out of vocab (oov) words
sentences = update_dataset(sentences, vocab)
# save updated dataset
filename = 'fren.pkl'
save_clean_sentences(sentences, filename)
# check the sentences
for i in range(10):
    print(sentences[i])
