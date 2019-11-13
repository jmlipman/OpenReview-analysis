from utils import *

papers = load_papers("data/iclr2020.h5py")

###############################
# Find top T shortest reviews #
###############################

T = 10
data = [] # List containing min_review_words
for i, paper in enumerate(papers):
    lowest_rev = 9999
    for rev in paper.reviews:
        if rev.review_words < lowest_rev:
            lowest_rev = rev.review_words
    data.append(lowest_rev)
data = np.array(data)
idx = np.argsort(data)
print("")
print(" > Shortests reviews")
for i in idx[:T]:
    print("{} {}. Words: {}".format(papers[i].url, papers[i].title, data[i]))

#####################################################
# Find the T most common words used in the abstract #
#####################################################

# key: word, value: (word id, count)
dictionary = {}
# idx: word id, value: word
id2word = []
for paper in papers:
    words = re.findall("[a-zA-Z]+", paper.abstract)
    for w in words:
        w = w.lower()
        if not w in dictionary.keys():
            dictionary[w] = [len(dictionary), 0]
            id2word.append(w)
        dictionary[w][1] += 1

data = []
for v in dictionary.values():
    data.append(v)
data = np.array(data)
# The most common first
idx = data[np.argsort(data[:,1])[::-1]][:,0]

T = 20
stopwords = ["the", "of", "to", "a", "and", "in", "that", "is", "on", "for", "we", "with", "by", "this", "as", "are", "can", "our", "an", "which", "be", "such", "from", "it", "has", "or", "more", "have"]
i, c = 0, 0
print("")
print(" > Most common words in the abstracts")
while i < len(idx) and c < T:
    w = id2word[idx[i]]
    if not w in stopwords:
        c += 1
        print("{} ({} times)".format(w, dictionary[w][1]))
    i += 1

######################################################
# Find the T least common words used in the abstract #
######################################################

# key: word, value: (word id, count)
dictionary = {}
# idx: word id, value: word
id2word = []
for paper in papers:
    words = re.findall("[a-zA-Z]+", paper.title)
    for w in words:
        w = w.lower()
        if not w in dictionary.keys():
            dictionary[w] = [len(dictionary), 0]
            id2word.append(w)
        dictionary[w][1] += 1

data = []
for v in dictionary.values():
    data.append(v)
data = np.array(data)
# The most common first
idx = data[np.argsort(data[:,1])][:,0]

T = 20
i, c = 0, 0
print("")
print(" > Least common words in the titles")
for i in range(T):
    w = id2word[idx[i]]
    print("{} ({} times)".format(w, dictionary[w][1]))
