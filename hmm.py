from nltk import sent_tokenize, word_tokenize
from nltk.tag import hmm
import random
from re import findall


def hidden_markov_model(text, number_of_hidden_states, number_of_iterations, number_of_words_to_generate):
    """
    Creates a text (list of words including punctuation, start- and end-of-sentence marks) based on the text
    from the function's arguments using hidden Markov models.

    Args:
        text: The text on which the output text is based (string).
        number_of_hidden_states: The number of hidden states (integer).
        number_of_iterations: The number of iterations of the hidden Markov model's training (integer).
        number_of_words_to_generate: The number of words (including start- and end-of-sentence marks) to generate
            (integer).

    Returns:
        A list of words (strings) including punctuation, start- and end-of-sentence marks generated using hidden Markov
        models and based on the text from the function's arguments.
        """
    tokens = [word for sentence in [["начало предложения"] + word_tokenize(sentence) + ["конец предложения"]
                                    for sentence in sent_tokenize(''.join(findall(r'[\w\s.?!,;:]',
                                                                                                ''.join(findall(r'\D',
                                                                                                                text)))))] for word in sentence]
    model = hmm.HiddenMarkovModelTrainer(range(number_of_hidden_states), set(tokens))

    batches = [[[t_] for t_ in tokens[i:i + 8]] for i in range(0, len(tokens), 8)]
    tagger = model.train_unsupervised(batches, max_iterations=number_of_iterations)
    return tagger.random_sample(random, number_of_words_to_generate)
