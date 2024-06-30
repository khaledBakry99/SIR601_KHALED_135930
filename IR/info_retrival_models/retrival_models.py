import math
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

language = ''
algorithm_type = ''
docs_number = 0
documents = dict()
documents['query'] = ''


def stem_words(sentence, language):
    words = word_tokenize(sentence)
    stemmer = PorterStemmer()
    if language == 'Arabic':
        stemmer = SnowballStemmer("arabic")
    stemmed_words = list(set([stemmer.stem(word) for word in words]))
    return stemmed_words


def stem(word, language):
    stemmer = PorterStemmer()  # language = 'English'
    if language == 'Arabic':
        stemmer = SnowballStemmer("arabic")
    return stemmer.stem(word)


def build_term_document_frequency(docs):
    term_document = dict(dict())
    for doc_name, doc_content in docs.items():
        words = word_tokenize(doc_content)
        for word in words:
            term = stem(word, language)
            if term not in term_document:
                term_document[term] = {doc_name: 1}
            elif doc_name not in term_document[term]:
                term_document[term][doc_name] = 1
            else:
                term_document[term][doc_name] += 1

    return term_document


def weighing_tf_idf(docs):
    term_doc_freq = build_term_document_frequency(docs)
    max_doc_freq = dict()
    for doc_name in docs.keys():
        max_doc_freq[doc_name] = 0
        for term in term_doc_freq.keys():
            if doc_name in term_doc_freq[term]:
                max_doc_freq[doc_name] = max(max_doc_freq[doc_name], term_doc_freq[term][doc_name])

    idf_term = dict()
    for term, doc_value in term_doc_freq.items():
        df = len(doc_value) - ('query' in term_doc_freq[term])
        if df == 0:  # term only in the query
            idf_term[term] = 0
        else:
            idf_term[term] = math.log2(len(docs) / df)

    term_doc_tf_idf = term_doc_freq.copy()
    for term, doc_value in term_doc_tf_idf.items():
        for doc_name, freq in doc_value.items():
            term_doc_tf_idf[term][doc_name] = (freq / max_doc_freq[doc_name]) * idf_term[term]
    return term_doc_tf_idf


def calculate_length(term_doc):
    length = dict()
    for term, doc_weight in term_doc.items():
        for doc_name, weight in doc_weight.items():
            if doc_name not in length:
                length[doc_name] = 0
            length[doc_name] += pow(term_doc[term][doc_name], 2)
    for doc_name, value in length.items():
        length[doc_name] = math.sqrt(value)
    return length


def vector_model(docs):
    tf_idf_term_doc = weighing_tf_idf(docs)
    query_terms = stem_words(docs['query'], language)

    length = calculate_length(tf_idf_term_doc)

    # Query terms not found in any document
    if 'query' not in length or length['query'] == 0:  # ADD
        return  # ADD

    similarity = {key: 0 for key in docs.keys()}
    for term in query_terms:
        for doc_name, tfidf in tf_idf_term_doc[term].items():
            similarity[doc_name] += tf_idf_term_doc[term]['query'] * tfidf / (length['query'] * length[doc_name])

    # similarity.pop('query')
    print(similarity)
    similarity = {doc_name: value for doc_name, value in similarity.items() if
                  value > 1e-7 and doc_name != 'query'}  # ADD
    sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True))
    print(sorted_similarity)
    return sorted_similarity


def extended_boolean_model(docs):
    term_doc_freq = build_term_document_frequency(docs)
    query_terms = stem_words(docs['query'], language)
    terms_number = len(query_terms)

    similarity = {doc_name: 0 for doc_name in docs.keys()}
    for term in query_terms:
        for doc_name in docs.keys():
            if doc_name not in term_doc_freq[term]:
                similarity[doc_name] += 1

    for doc_name in docs.keys():
        similarity[doc_name] = 1 - math.sqrt(similarity[doc_name] / terms_number)
        if abs(similarity[doc_name]) < 1e-10:
            similarity.pop(doc_name, None)

    similarity = {doc_name: value for doc_name, value in similarity.items() if value > 1e-7 and doc_name != 'query'} #ADD
    sorted_similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True))

    return sorted_similarity


def boolean_model(docs):
    term_doc_freq = build_term_document_frequency(docs)
    query_terms = stem_words(docs['query'], language)
    terms_number = len(query_terms)

    similarity = {doc_name: 0 for doc_name in docs.keys()}
    for term in query_terms:
        for doc_name, freq in term_doc_freq[term].items():
            similarity[doc_name] += 1

    similarity = {doc_name: value for doc_name, value in similarity.items() if
                  value == terms_number and doc_name != 'query'}

    return similarity


def red_coloring(sentence):
    reset_color_code = '\033[0m'  # Reset ANSI escape code (to default color)
    red_color_code = '\033[91m'  # ANSI escape code for red color
    # return (red_color_code + sentence + reset_color_code)
    return ('<span class="highlight">{' + sentence + '}</span>')

# X AND Y OR Z

def show_results(docs, language, algorithm_type):
    similarity = dict()
    if algorithm_type == 'boolean':
        similarity = boolean_model(docs)
    elif algorithm_type == 'extended_boolean':
        similarity = extended_boolean_model(docs)
    else:
        similarity = vector_model(docs)

    query_terms = stem_words(docs['query'], language)
    results = []
    for doc_name, sim in similarity.items():
        print(f"Ratio of similarity between query and document {doc_name} = {sim}")
        highlighted_doc = ''
        for word in word_tokenize(docs[doc_name]):
            if stem(word, language) in query_terms:
                highlighted_doc += f'<span class="highlight">{word}</span> '
                # print(red_coloring(word), end=' ')
            else:
                highlighted_doc += f'{word} '
                # print(word, end=' ')
        results.append({
            "doc_name": doc_name,
            "doc_sim": sim,
            "doc_content": highlighted_doc
        })
    # print()
    # print()
    # print(results)

    return results


def query_function(language, algorithm_type, user_documents, query):
    language = language
    algorithm_type = algorithm_type
    documents = user_documents
    documents['query'] = query

    return show_results(documents, language, algorithm_type)
