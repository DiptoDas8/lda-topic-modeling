from random import randint, uniform
from copy import deepcopy
from operator import attrgetter


''' 
    Number of topics K
    Number of documents D
    Number of entries in vocabulary V
    Total number of words in corpus (collection of  ܦdocuments) N
    Word i in the corpus is w_i
    Number of words generated from topic t in document `del' is n_del_t
    Pseudo count of words generated from any topic in document `del' is alpha
    Number of times word w is generated from topic t in the corpus is n_t_w
    Pseudo count of times any word is generated from topic t is eta
    Fraction of words generated from topic (proportion of topic) t in document del is theta_del_t
    Probability of a word w in topic t is beta_t_w
    An estimate of theta_del_t using
    Probability of a word w in topic t is beta_t_w
'''

# number_of_documents = 200
number_of_documents = 10
# number_of_topics = 20
number_of_topics = 2
# top_freq_count = 5
top_freq_count = 3

''' LDA parameters '''
alpha = 50 / number_of_topics
eta = 0.1



class Model:
    '''The built model structure'''
    topic = 0
    freq = 0
    word = ''

    def __init__(self, topic, freq, word):
        self.topic = topic
        self.freq = freq
        self.word = word

    def __str__(self):
        return 'topic_' + str(self.topic) + ': ' + self.word + '( ' + str(self.freq) + ' )'


def lda(max_iterations, burn_in, lag):
    '''
    :param max_iterations:
    :param burn_in:
    :param lag:
    :return:

    '''
    print(max_iterations, burn_in, lag, alpha, eta, number_of_topics, top_freq_count)

    # initialize topic indices
    topiclist = []

    # initialize word indices
    wordlist = []

    topics_in_document = [[0 for i in range(number_of_topics)] for j in range(number_of_documents)]
    words_in_topic = [[] for j in range(number_of_topics)]

    trackdoc = []
    for doc in range(number_of_documents):
        # print(doc)
        topics = []
        filename = '../data/20newsgroups/' + str(doc + 1)
        # filename = '../data/artificial/' + str(doc + 1)
        string = open(filename, 'r').read().replace('\n', '')

        words = string.split()
        for word in words:
            top = randint(0, number_of_topics - 1)  # python randint is inclusive, i.e. a <= retval <= b
            words_in_topic[top].append(word)
            topics.append(top)
            trackdoc.append(doc)

        unique_topics = set(topics)

        # print(len(topics_in_document), len(topics_in_document[0]))
        for topic in unique_topics:
            topics_in_document[doc][topic] = topics.count(topic)

        wordlist = wordlist + words
        topiclist = topiclist + topics

    number_of_words = len(wordlist)
    vocabulary = list(set(wordlist))
    number_of_entries_in_vocab = len(vocabulary)
    vocab_under_topic = [[0 for i in range(number_of_entries_in_vocab)] for j in range(number_of_topics)]

    # for t in range(number_of_topics):
    #     print(words_in_topic[t])

    for topic in range(number_of_topics):
        words = words_in_topic[topic]
        unique_words = set(words)
        for word in unique_words:
            vocab_under_topic[topic][vocabulary.index(word)] = words.count(word)

    # Initialize 1 x K array of probabilities P (to zero)
    probabilities = [0.0 for i in range(number_of_topics)]

    states = []
    states.append(vocab_under_topic)

    sum_of_topics_in_doc = [[0 for i in range(number_of_topics)] for j in range(number_of_documents)]
    for y in range(number_of_documents):
        sum_of_topics_in_doc[y][0] = topics_in_document[y][0]
        for x in range(1, number_of_topics):
            sum_of_topics_in_doc[y][x] = sum_of_topics_in_doc[y][x - 1] + topics_in_document[y][x]

    sum_of_vocub_under_topic = deepcopy(vocab_under_topic)
    for y in range(number_of_topics):
        for x in range(1, number_of_entries_in_vocab):
            sum_of_vocub_under_topic[y][x] = sum_of_vocub_under_topic[y][x - 1] + vocab_under_topic[y][x]

    for r in range(max_iterations):
        # print('iter: ', r)
        for i in range(number_of_words):
            word = wordlist[i]
            topic = topiclist[i]
            delta = trackdoc[i]

            topics_in_document[delta][topic] -= 1
            sum_of_topics_in_doc[delta][topic] -= 1

            v = vocabulary.index(word)
            vocab_under_topic[topic][v] -= 1
            sum_of_vocub_under_topic[topic][v] -= 1

            for t in range(number_of_topics):
                # print(number_of_topics, alpha, sum_of_topics_in_doc)
                theta = (alpha + topics_in_document[delta][t]) / (
                        number_of_topics * alpha + sum(topics_in_document[delta]))
                beta = (eta + vocab_under_topic[t][v]) / (
                        number_of_entries_in_vocab * eta + sum_of_vocub_under_topic[t][v])
                probabilities[t] = theta * beta

            sum_of_prob = sum(probabilities)
            for i in range(len(probabilities)):
                probabilities[i] /= sum_of_prob

            # sample t ~ probabilities
            cummulative_probabilities = [0.0]
            for t in range(len(probabilities)):
                cummulative_probabilities.append(cummulative_probabilities[t] + probabilities[t])

            rand = uniform(0.0, 1.0)
            changed_topic = 0
            for t in range(len(cummulative_probabilities)):
                if cummulative_probabilities[t] <= rand < cummulative_probabilities[t + 1]:
                    changed_topic = t
                    break

            topiclist[i] = changed_topic
            topics_in_document[delta][changed_topic] += 1
            sum_of_topics_in_doc[delta][changed_topic] += 1

            vocab_under_topic[changed_topic][v] += 1
            sum_of_vocub_under_topic[changed_topic][v] += 1

        if r > burn_in and r % lag == 0:
            state = states[len(states) - 1]
            for i in range(number_of_topics):
                for j in range(number_of_entries_in_vocab):
                    state[i][j] += vocab_under_topic[i][j]

            states.append(state)

    last_state = states[-1]
    average = [[0.0 for i in range(number_of_entries_in_vocab)] for j in range(number_of_topics)]
    for y in range(number_of_topics):
        for x in range(number_of_entries_in_vocab):
            average[y][x] = last_state[y][x] * 1.0 / len(states)

    models = [None for i in range(number_of_topics)]
    for t in range(number_of_topics):
        models[t] = []
        for v in range(number_of_entries_in_vocab):
            model = Model(t, average[t][v], vocabulary[v])
            models[t].append(model)
        models[t].sort(key=attrgetter('freq'), reverse=True)

    record = []
    # print('number of iterations: ', max_iterations, ', burn-in: ', burn_in, ', lag: ', lag)
    for t in range(0, number_of_topics):
        entry = models[t]
        line = []
        for i in range(0, top_freq_count):
            line.append(entry[i].word)
        # print('%d :'%(t),line)
        record.append(line)

    print('hi')
    return record


def set_params(m, b, l, a, e, t, f):
    # print(m, b, l, a, e, t, f)
    global alpha, eta, number_of_topics, top_freq_count
    alpha = a/t
    eta = e
    number_of_topics = t
    top_freq_count = f
    return lda(m, b, l)
    # return

# if __name__ == '__main__':
#     lda(1000, 100, 5)
