from collections import defaultdict
import numpy as np
import pickle
import math
import os
import time
import json
import japanese
from copy import deepcopy, copy
import sys
import operator
sys.path.append('..')
from config import root_path, data_path, train_path, experiment_path
from model_ngram import NGramModel
from train.data import Vocab

class Node():
    def __init__(self, s, l, idx, word, oov_prob=0.0):
        self.start_idx = s  # start index of word
        self.reading_length = l  # length of the reading NOT the word
        self.word_idx = idx  # the index of the node in the output softmax layer
        self.word = word  # word of the node

    def __repr__(self):
        return str((self.start_idx, self.word))

class Path():
    """A class that contains all relevant information about each path through the lattice."""
    def __init__(self, node):
        # init with path start '<eos>'
        self.nodes = [node]
        self.neg_log_prob = 0.0  # accumulated neg log of the each node to node prob becomes the path neg log prob

    def __str__(self):
        return ' '.join(['{}'.format(x.word) for x in self.nodes]) + ': {}'.format(self.neg_log_prob)

class NGramDecoder():
    def __init__(self, experiment_id, ngram_order=3):
        self.config = json.loads(open(os.path.join(experiment_path, str(experiment_id), 'config.json'), 'rt').read())
        vocab = Vocab(self.config['vocab_size'])
        self.i2w = vocab.i2w
        self.w2i = vocab.w2i

        # full lexicon and reading dictionary covers all the vocab
        # that includes oov words to the model
        self.full_lexicon = pickle.load(open(os.path.join(root_path, 'data', 'lexicon.pkl'), 'rb'))
        self.full_reading_dict = pickle.load(open(os.path.join(root_path, 'data', 'reading_dict.pkl'), 'rb'))

        self.model = NGramModel(ngram_file='lm3', ngram_order=ngram_order)
        
        self.perf_sen = 0
        self.perf_log = []

    def _check_oov(self, word):
        return word not in self.w2i.keys()

    def _build_lattice(self, input, use_oov=False):
        def add_node_to_lattice(i, sub_token, id, word, prob):
            node = Node(i, len(sub_token), id, word, prob)  # share the node in both lookup table
            backward_lookup[i + len(sub_token)].append(node)

        # backward_lookup keeps the words that ends at a frame
        # e.g. the input A/BC/D, 0 is preserved for <eos>
        # 0        1        2        3         4
        # <eos>    A                BC         D
        backward_lookup = defaultdict(lambda: [])
        eos_node = [Node(-1, 1, self.w2i['<eos>'], '<eos>')]
        backward_lookup[0] = eos_node

        for i, token in enumerate(input):
            for j in range(len(input) - i):
                sub_token = input[i: i + j + 1]
                if sub_token in self.full_reading_dict.keys():
                    for lexicon_id in self.full_reading_dict[sub_token]:
                        word = self.full_lexicon[lexicon_id][0]
                        oov = self._check_oov(word)
                        if oov:
                            # skip oov in this experiment,
                            # note that oov affects conversion quality
                            continue
                        prob = 0.0
                        id = self.w2i[word]
                        add_node_to_lattice(i, sub_token, id, word, prob)

        return backward_lookup

    def _build_current_frame(self, nodes, frame, idx):
        # frame 0 contains one path that has eos_node
        if idx == 0:
            frame[0] = [Path(nodes[0])]
            return

        # connect each nodes to its previous best paths, also calculate the new path probability
        frame[idx] = []
        for node in nodes:
            for prev_path in frame[node.start_idx]:
                cur_paths = copy(prev_path)  # shallow copy to avoid create dup objects
                cur_paths.nodes = copy(prev_path.nodes)
                cur_paths.nodes.append(node)
                words = [node.word for node in cur_paths.nodes]
                start_time = time.time()
                prob = self.model.predict(words)
                self.perf_log.append(time.time() - start_time)
                cur_paths.neg_log_prob += prob
                frame[idx].append(cur_paths)

    def decode(self, input, topN=10, beam_width=10, use_oov=False, vocab_select=False, samples=0, top_sampling=False, random_sampling=False):
        backward_lookup = self._build_lattice(input, use_oov)

        frame = {}
        for i in range(len(input) + 1):
            b_nodes = backward_lookup[i]
            self._build_current_frame(b_nodes, frame, i)

            if beam_width is not None:
                frame[i].sort(key=lambda x: x.neg_log_prob)
                frame[i] = frame[i][:beam_width]

            # self._batch_predict(frame[i])

        output = [(x.neg_log_prob, [n.word for n in x.nodes if n.word != "<eos>"]) for x in frame[len(input)]]
        
        self.perf_sen += 1
        
        return output[:topN]

if __name__ == "__main__":
    decoder = NGramDecoder(experiment_id=10)
    start_time = time.time()
    # result = decoder.decode('キョーワイーテンキデス', topN=10, beam_width=10, use_oov=True)
    result = decoder.decode('xianshi', topN=10, beam_width=10, use_oov=True)
    for item in result:
        print(item)
    print("--- %s seconds ---" % (time.time() - start_time))
