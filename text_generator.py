import random

class MarkovTextGenerator:
    def __init__(self):
        self.word_dict = {}

    def train(self, text):
        words = text.split()
        for i in range(len(words) - 1):
            if words[i] not in self.word_dict:
                self.word_dict[words[i]] = []
            self.word_dict[words[i]].append(words[i + 1])

    def generate_text(self, start_word, length):
        if start_word not in self.word_dict:
            return "Start word not found in training data."

        current_word = start_word
        generated_words = [current_word]

        for _ in range(length - 1):
            next_words = self.word_dict.get(current_word)
            if not next_words:
                break
            current_word = random.choice(next_words)
            generated_words.append(current_word)

        return ' '.join(generated_words)
