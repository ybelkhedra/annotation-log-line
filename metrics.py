from difflib import SequenceMatcher  
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from Levenshtein import distance as levenshtein_distance
from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
import jaro
from collections import Counter


def python_diff_str(s1, s2):
    return SequenceMatcher(a=s1, b=s2).ratio()


def cosine_similarity_str(s1, s2):
    corpus = [s1, s2]
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    
    similarity = cosine_similarity(X)[0][1]
    
    return similarity


def levenshtein_distance_str(s1, s2):
    return 1 - levenshtein_distance(s1, s2) / max(len(s1), len(s2))


def SmithWaterman_str(s1, s2):
    #return the Smith-Waterman score beween between 0 and 1
    return SmithWaterman().get_raw_score(s1, s2) / max(len(s1), len(s2))

def MongeElkan_str(s1, s2):
    return MongeElkan().get_raw_score([s1], [s2])


def jarowinkler_str(s1, s2):
    return jaro.jaro_winkler_metric(s1, s2)


def jaccard_str(s1, s2):
    intersection = set(s1) & set(s2)
    union = set(s1) | set(s2)
    return len(intersection) / len(union)


def ngram_str(s1, s2, n=3):
    def generate_ngrams(string, n):
        return [string[i:i+n] for i in range(len(string)-n+1)]
    
    ngrams1 = generate_ngrams(s1, n)
    ngrams2 = generate_ngrams(s2, n)
    
    count1 = Counter(ngrams1)
    count2 = Counter(ngrams2)
    
    common_occurrences = sum((count1 & count2).values())
    
    similarity = common_occurrences / (len(ngrams1) + len(ngrams2) - common_occurrences)
    
    return similarity


def LCS_str(s1, s2):
    m, n = len(s1), len(s2)
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    lcs_length = dp[m][n]
    
    similarity = lcs_length / max(len(s1), len(s2))
    
    return similarity


if __name__ == "__main__":
    s1, s2 = "aaa", "jjjjjjjjjjjjj"
    s1, s2 = "Hello world", "Hellu world"
    print("Python diff distance:", python_diff_str(s1, s2))
    print("Cosine similarity:", cosine_similarity_str(s1, s2))
    print("Levenshtein distance:", levenshtein_distance_str(s1, s2))
    print("Smith Waterman distance:", SmithWaterman_str(s1, s2))
    print("Mongel Elkan distance:", MongeElkan_str(s1, s2))
    print("Jaro winklers distance:", jarowinkler_str(s1, s2))
    print("Jaccard distance:", jaccard_str(s1, s2))
    print("Ngram distance:", ngram_str(s1, s2, 3))
    print("LCS distance:", LCS_str(s1, s2))