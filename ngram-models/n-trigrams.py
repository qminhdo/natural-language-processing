import sys, re

# python n-trigrams.py <input-file> <model-file>

input_file = "I am Sam. Sam I am" \
             "Hello' World"
input_file = "I am."

def filter_text(str):
    # Put * * before each sentence
    str = re.sub('^.*\.$', '* *', str)

    # Replace new line, commas and apostrophes with a space
    # str = re.sub('[\n,\']', ' ', str)

    # Mark end of sentence with <STOP>
    # str = re.sub('[.]', '<STOP>', str)
    # Replace accents and tildes with English equivalent

    # Replace double space
    return str

def read_file(filename):
    pass

def save_dict(output_filename):
    pass

def read_model(filename):
    pass

def compute_bigram_prob():
    pass

print(filter_text(input_file))