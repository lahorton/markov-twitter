"""Generate Markov text from text files."""

from random import choice
import sys
import twitter
import os
import string

api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# print(api.VerifyCredentials())


def open_and_read_file(file_path):
    """Takes multiple files as strings; return text as a single string.
    """
    text = " "

    for file in file_path:
        text_file = open(file)
        text = text + text_file.read()
        text_file.close()

    return text


def make_chains(text_string, n=2):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of "n" length of words
    (word1, word2 ...wordn)
    and the value would be a list of the word(s) that follow those
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]
    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = tuple(text_string.split())

    for i in range(len(words)-n):
        pair = words[i:i+n]

        if pair not in chains:
            chains[pair] = []

        chains[pair].append(words[i+n])
    return chains


def make_text(chains):
    """Return text from chains."""

    key = choice(list(chains.keys()))
    words = list(key)

    while key in chains:
        key_string = len(str(words))
        if key_string >= 280:
            break
        new = choice(chains[key])
        words.append(new)
        key = key[1:] + (new,)

    for i in reversed(range(len(words))):
        if words[i][-1] in '!.-?"':
            words = words[:i+1]
            break

    words[0] = words[0].capitalize()

    return " ".join(words)


def make_tweet(text):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    while True:
        input_text = open_and_read_file(text)
        chains = make_chains(input_text)
        random_text = make_text(chains)

        status = api.PostUpdate(random_text)
        print(random_text, "\n")

        more = input("Enter to tweet again [q to quit] > ").lower()

        if more == 'q':
            break


text = sys.argv[1:]

# # Open the file and turn it into one long string
# input_text = open_and_read_file(text)

# # Get a Markov chain
# chains = make_chains(input_text)

# # Produce random text
# random_text = make_text(chains)

make_tweet(text)
