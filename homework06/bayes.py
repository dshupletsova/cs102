import cs
import random
import string
import typing as tp
from collections import Counter, defaultdict
from math import log

from db import News, session


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.counters = defaultdict(lambda: defaultdict(int))
        self.words_set = set()
        self.class_counter = defaultdict(int)
        self.words_count = 0

    def fit(self, X, y):
        for xi, yi in zip(X, y):
            self.class_counter[yi] += 1
            for word in xi.split():
                self.counters[yi][word] += 1
                self.words_set.add(word)
                self.words_count += 1

    def predict(self, X):
        predicted = []
        for string in X:
            predicted.append(self._predict_class(string))
        return predicted

    def _predict_class(self, string):
        class_ind = None
        count_of_elements = sum(self.class_counter.values())
        best_val = float("-inf")
        for class_i in self.counters:
            curr_value = log(self.class_counter[class_i] / count_of_elements)
            for word in string.split():
                count_of_curr_word_in_class = self.counters[class_i][word]
                count_of_words_in_curr_class = sum(self.counters[class_i].values())
                curr_value += log(
                    (count_of_curr_word_in_class + self.alpha)
                    / (count_of_words_in_curr_class + self.alpha * len(self.words_set))
                )
            if best_val < curr_value:
                class_ind = class_i
                best_val = curr_value
        if class_ind is None:
            raise Exception("Classifier is not fitted")
        return class_ind

    def score(self, X_test, y_test):
        results = self.predict(X_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def label_news():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    for row in rows:
        row.label = random.choice(["good", "maybe", "never"])
        s.add(row)
        s.commit()


if __name__ == "__main__":
    with open("data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    print(X[0], "|||", y[0])
