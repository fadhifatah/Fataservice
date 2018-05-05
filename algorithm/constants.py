import os


class Constants:
    dir = os.path.dirname(__file__)


class Review(object):
    def __init__(self, rid, text, aspects: set, trainer):
        self.rid = rid
        self.text = text
        self.aspects = aspects
        self.trainer = trainer

        # accessing aspects
        self.food = self.aspects.get('FOOD', '-')
        self.price = self.aspects.get('PRICE', '-')
        self.service = self.aspects.get('SERVICE', '-')
        self.ambience = self.aspects.get('AMBIENCE', '-')

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.rid == other.rid

    def __hash__(self):
        return 31 * hash(self.rid) + 17 * hash(self.text)

    def __str__(self):
        return '================================================' + '\n' + self.rid + '  ' + self.trainer + '\n' + \
               self.text + '\n' + self.aspects.get('FOOD', '-') + '  ' + self.aspects.get('PRICE', '-') + '  ' + \
               self.aspects.get('SERVICE', '-') + '  ' + self.aspects.get('AMBIENCE', '-') + '\n'

    def add_trainer(self, trainer):
        self.trainer = self.trainer + " " + trainer
