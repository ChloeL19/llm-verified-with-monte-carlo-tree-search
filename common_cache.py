def select_with_scores(texts, scores, score_predicate, select):
    indices = [i for i in range(len(texts)) if score_predicate(scores[i])]
    if indices == []:
        return texts[0], scores[0]
    text = select([texts[i] for i in indices], indices)
    return text, [scores[i] for i in indices if text == texts[i]][0]

def create_score_predicate(f=lambda x: x):
    def fetch(x):
        score = f(x)
        return score is None or score > 0
    return fetch

def score_first(x):
    return x[0]

cache = {}
def create_caching_score_func(f):
    def fetch(x):
        if x in cache:
            return cache[x]
        else:
            y = f(x)
            cache[x] = y
            return y
    return fetch
