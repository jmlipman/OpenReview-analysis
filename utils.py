import numpy as np
import h5py, ast, re

def _decode(string):
    if type(string) == bytes or type(string) == np.bytes_:
        string = string.decode("utf8")
    string = re.sub(" +", " ", string)
    return string


class Review:
    def __init__(self, rating, experience, review, comments):
        self.rating = rating
        self.experience = _decode(experience)
        self.review = _decode(review)
        self.review_len = len(self.review)
        self.review_words = len(re.findall("[a-zA-Z]+", self.review))
        self.comments = [_decode(c) for c in comments]

class Paper:
    def __init__(self, title, abstract, tl_dr, keywords,
                 reviews, url, rating, decision, code):
        self.title = title
        self.abstract = _decode(abstract)
        self.tl_dr = _decode(tl_dr)
        self.keywords = [_decode(k) for k in keywords]
        self.reviews = reviews
        self.url = url
        self.rating = rating
        self.decision = decision
        self.code = _decode(code)

def load_papers(filename):
    f = h5py.File(filename, "r")
    papers = []
    for k in list(f.keys()): # Iterate over each paper
        reviews = ast.literal_eval(f[k]["reviews"].value)
        reviews = [Review(r["rating"], r["experience_assessment"], r["review"], r["comments"]) for r in reviews]

        papers.append(Paper(
            f[k]["title"].value,
            f[k]["abstract"].value,
            f[k]["tl_dr"].value,
            f[k]["keywords"].value,
            reviews,
            f[k]["url"].value,
            f[k]["rating"].value,
            f[k]["decision"].value,
            f[k]["code"].value
        ))
    return papers


