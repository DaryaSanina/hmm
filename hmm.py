from math import ceil
import matplotlib.pyplot as plt
from nltk import sent_tokenize, word_tokenize
from nltk.tag import hmm
import random
from re import findall


def hidden_markov_model(text, number_of_hidden_states, number_of_iterations, number_of_words_to_generate):
    """Creates a text (list of words including punctuation, start- and end-of-sentence marks) based on the text
    from the function's arguments using hidden Markov models.

    Args:
        text: The text on which the output text is based (string).
        number_of_hidden_states: The number of hidden states of the hidden Markov model (integer).
        number_of_iterations: The number of iterations of the hidden Markov model's training (integer).
        number_of_words_to_generate: The number of words (including start- and end-of-sentence marks) to generate
            (integer).

    Returns:
        A list of words (strings) including punctuation, start- and end-of-sentence marks generated using hidden Markov
        models and based on the text from the function's arguments.
        """
    # Getting tokens from the text
    tokens = [["начало предложения"] + word_tokenize(sentence) + ["конец предложения"]
              for sentence in sent_tokenize(''.join(findall(r'[\w\s.?!,;:]', ''.join(findall(r'\D', text)))))]

    # Creating the hmm
    model = hmm.HiddenMarkovModelTrainer(range(number_of_hidden_states),
                                         set([word for sentence in tokens for word in sentence]))

    batches = [[[word] for word in sentence] for sentence in tokens]  # Splitting the text into n-grams (sentences)
    tagger = model.train_unsupervised(batches, max_iterations=number_of_iterations)  # Training the model
    return tagger.random_sample(random, number_of_words_to_generate)


def quality_control(text, number_of_iterations, list_of_hidden_state_numbers, dest_filename):
    """For each number of hidden states trains a hidden Markov model on the first half of the text from the function's
    arguments and checks the average entropy of this model on the second half of the text from the function's arguments,
    then creates a graph with sorted hidden state numbers as X-axis and the average entropy as Y-axis and saves
    the graph to a file with its name from the function's arguments.

    Args:
        text: The text, the first half of that is a training set and the second half - a testing set (string).
        number_of_iterations: The number of iterations of the hidden Markov model's training (integer).
        list_of_hidden_state_numbers: The list of numbers of hidden states of hidden Markov models (list of integers).
        dest_filename: The name of the file where the function saves the graph.

    Returns: None
    """
    # Getting tokens from the text
    tokens = [["начало предложения"] + word_tokenize(sentence) + ["конец предложения"]
              for sentence in sent_tokenize(''.join(findall(r'[\w\s.?!,;:]', ''.join(findall(r'\D', text)))))]

    # Splitting the tokens into a training set and a testing set
    # and deleting all the words that are not in the training set from the testing set
    training_set = tokens[:ceil(len(tokens) / 2):]
    testing_set = [[testing_set_word for testing_set_word in testing_set_sentence
                    if testing_set_word in [training_set_word for training_set_sentence in training_set
                                            for training_set_word in training_set_sentence]]
                   for testing_set_sentence in tokens[ceil(len(tokens) / 2)::]]

    list_of_entropy = []
    for number_of_hidden_states in sorted(list_of_hidden_state_numbers):
        # Creating the hmm
        model = hmm.HiddenMarkovModelTrainer(range(number_of_hidden_states),
                                             set([word for sentence in training_set for word in sentence]))

        # Training the model
        batches = [[[word] for word in sentence] for sentence in training_set]
        tagger = model.train_unsupervised(batches, max_iterations=number_of_iterations)

        # Counting the entropy
        entropy = [tagger.entropy([[word] for word in sentence]) for sentence in testing_set]
        list_of_entropy.append(sum(entropy) / len(entropy))

    plt.plot(sorted(list_of_hidden_state_numbers), list_of_entropy)  # Drawing the graph
    plt.savefig(dest_filename)  # Saving the graph
