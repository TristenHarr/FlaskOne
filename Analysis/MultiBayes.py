from Analysis.DataPuller import Table, DataBaseSearch, Statement
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import random


class NaiveBayes(object):

    def __init__(self, database, table, text_source, category=None):
        self.con = DataBaseSearch(database)
        self.table = Table(table=table, rows=[text_source])
        search_for = Statement(selection='lang', parameters="'en'")
        self.table.commit_statement(search_for)
        self.frame = self.con.get_DataFrame(self.table.query)
        self.text = list(self.frame[text_source])
        self.type = [category for item in self.text]
        self.results = zip(self.text, self.type)

class DataModel(object):

    def __init__(self):
        self.model = []
        self.categories = []

    def add_item(self, database, table, text_source, type):
        temp = NaiveBayes(database, table, text_source, type)
        self.model.extend(list(temp.results))
        self.categories.append(type)

    def preperation(self):
        random.shuffle(self.model)
        my_words = []
        my_numbers = []
        for item in self.model:
            my_words.append(item[0])
            my_numbers.append(self.categories.index(item[1]))
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(my_words[0:1500])
        from sklearn.feature_extraction.text import TfidfTransformer
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        clf = MultinomialNB().fit(X_train_tfidf, my_numbers[0:1500])

        docs_new = my_words[1500:]
        X_new_counts = count_vect.transform(docs_new)
        X_new_tfidf = tfidf_transformer.transform(X_new_counts)

        import numpy as np
        predicted = clf.predict(X_new_tfidf)
        print(my_numbers[1500:])
        print(list(zip(my_numbers[1500:], predicted)))

        for doc, category, thing in zip(docs_new, predicted, my_numbers[1500:]):
            print("Plain Text: {}\nActual Category: {}\nPrediction: {}".format(doc, self.categories[category], self.categories[thing]))

        print(np.mean(predicted == my_numbers[1500:]))


my_test = DataModel()
my_test.add_item('Society', 'pets', 'plain_text', 'Pets')
my_test.add_item('Society', 'politics', 'plain_text', 'Politics')
my_test.preperation()
