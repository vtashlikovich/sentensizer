"""Dictionary class implementation."""
import json

class Dict:
    """Implementation of words dictionary."""

    def __init__(self):
        self.dictionary = {}

    def get_items(self):
        return self.dictionary.items()

    def delete(self, id):
        del self.dictionary[id]

    def print(self):
        print(self.dictionary)

    def get_hyperonims(self):
        # returns a list of unique dict values
        return list(set(self.dictionary.values()))
