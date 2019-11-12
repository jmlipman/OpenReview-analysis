# This script saves review-related information in a h5py-format file.

from selenium.webdriver import Firefox # pip install selenium
import time
import numpy as np
import h5py

def clean_str(string):
    """This function replace unicode characters by ?.
    """
    return string.encode("ascii", errors="replace")

def parse_notefield(string):
    string = string[:-1].lower() # Lower case, remove last colon
    string = string.replace(" ", "_")
    return string


file_URLs = "urls_iclr2020.txt"
file_output = "iclr2020.h5py"

with open(file_URLs, "r") as f:
    urls = f.read().split("\n")[:-1]

browser = Firefox()

urls = urls[:10]
f = h5py.File(file_output, "w")
for i, url in enumerate(urls):
    print("{}/{}".format(i+1, len(urls)))
    paper = {}

    browser.get(url)
    time.sleep(3)

    # OpenReview.net URL
    paper["url"] = url

    # Title of the paper
    paper["title"] = browser.find_element_by_xpath("//h2").text

    # Initializing
    for k in ["keywords", "abstract", "tl_dr", "code", "decision", "rating"]:
        paper[k] = ""

    # Submission
    submission_ = browser.find_elements_by_xpath("//main/div[@class='note panel']")[0]
    key_ = submission_.find_elements_by_class_name("note_content_field")
    value_ = submission_.find_elements_by_class_name("note_content_value")
    for k, v in zip(key_, value_):
        k = k.text[:-1].lower().replace(" ", "_") # Clean

        if k == "keywords":
            paper[k] = [clean_str(vv) for vv in v.text.split(", ")]
        elif k == "tl_dr" or k == "abstract" or k == "code":
            paper[k] = clean_str(v.text)

    reviews_ = browser.find_elements_by_xpath("//main/div[@id='note_children']/div[@class='note_with_children comment-level-odd']")
    reviews = []
    # Iterate over all the reviews
    for review_ in reviews_:


        # TODO add "decision"
        # 1) Save elements of the review
        is_review = False
        key_ = review_.find_elements_by_class_name("note_content_field")
        value_ = review_.find_elements_by_class_name("note_content_value")
        rev = {} # Here I will save the review
        for k, v in zip(key_, value_):
            k = k.text[:-1].lower().replace(" ", "_") # Clean

            if k == "rating":
                rev[k] = int(v.text[0])
                is_review = True
            elif k == "experience_assessment" or k == "review" or k == "confidence":
                rev[k] = clean_str(v.text)
            elif k == "decision":
                paper[k] = clean_str(v.text)

        if not is_review:
            continue

        # 2) Save comments of the review
        # Nested comments will be put together as if they are in the same level
        c1_ = review_.find_element_by_class_name("children")
        comments_ = c1_.find_elements_by_class_name("note_with_children")
        comments = []
        for c_ in comments_:
            # In reality there might be more than one "element", when there are
            # nested
            try: # This may raise an error if the "Comment" is deleted
                 # Because then it does not have note_content_value
                comm = clean_str(c_.find_element_by_class_name("note_content_value").text)
                comments.append(comm)
            except:
                pass
        rev["comments"] = comments

        # 3) Save the review
        reviews.append(rev)
    paper["reviews"] = str(reviews)
    paper["rating"] = np.mean([rev["rating"] for rev in reviews])

    # I have to write this at the end because h5py does not let me initialize
    # variables and later fill them
    paper_ = f.create_group(str(i))
    for k in paper.keys():
        paper_[k] = paper[k]

f.close()

print("Finished")
