import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability = {}

    if len(corpus[page]) > 0:
        for p in corpus:
            if p in corpus[page]:
                probability[p] = ((1 - damping_factor)/(len(corpus))) + (damping_factor/len(corpus[page]))
            else:
                probability[p] = (1 - damping_factor) / (len(corpus))
    else:
        for p in corpus:
            probability[p] = 1 / len(corpus)
    # print(probability.keys())
    # print(probability.values())
    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    current_page = None
    for i in range(n):
        if current_page == None:
            current_page = random.choice(list(corpus.keys()))
        else:
            prob = transition_model(corpus, current_page, damping_factor)
            current_page = random.choices(list(prob.keys()), weights=list(prob.values()), k=1)[0]
        try:
            if page_rank[current_page]:
                page_rank[current_page] += 1
        except KeyError:
            page_rank[current_page] = 1
        i += 1
    for p in page_rank:
        page_rank[p] = page_rank[p]/10000
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    PR = {}
    for page in corpus:
        PR[page] = 1/len(corpus)

    while True:
        check = 0
        current_pr = PR.copy()

        for page in corpus:
            link_value = 0
            for link in corpus:
                if len(corpus[link]) == 0:
                    link_value += current_pr[link] / len(corpus)
                elif page in corpus[link]:
                    link_value += current_pr[link] / len(corpus[link])
            PR[page] = ((1-damping_factor) / len(corpus)) + (damping_factor * link_value)

            if abs(current_pr[page] - PR[page]) < 0.001:
                check += 1

        if check == len(corpus):
            PR = current_pr
            break
    return PR


if __name__ == "__main__":
    main()
