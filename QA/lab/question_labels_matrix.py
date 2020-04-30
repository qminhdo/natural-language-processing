import pandas as pd
import os
import tensorflow as tf
import pickle
import re


"""
Create a train and test dataframes wit all label column
"""
dir = "./data/cogcomp/train_set_categorized"
filenames = []
for dirname, dirnames, filenames_ in os.walk(dir):
    for filename in filenames_:
        filenames.append(filename)

# Filenames has to be in this order for matrix to work properly
# we will refer the label by its index number
filenames = ['ABBR_abb.txt', 'ABBR_exp.txt', 'DESC_def.txt', 'DESC_desc.txt', 'DESC_manner.txt', 'DESC_reason.txt',
             'ENTY_animal.txt', 'ENTY_body.txt', 'ENTY_color.txt', 'ENTY_cremat.txt', 'ENTY_currency.txt',
             'ENTY_dismed.txt', 'ENTY_event.txt', 'ENTY_food.txt', 'ENTY_instru.txt', 'ENTY_lang.txt',
             'ENTY_letter.txt', 'ENTY_other.txt', 'ENTY_plant.txt', 'ENTY_product.txt', 'ENTY_religion.txt',
             'ENTY_sport.txt', 'ENTY_substance.txt', 'ENTY_symbol.txt', 'ENTY_techmeth.txt', 'ENTY_termeq.txt',
             'ENTY_veh.txt', 'ENTY_word.txt', 'HUM_desc.txt', 'HUM_gr.txt', 'HUM_ind.txt', 'HUM_title.txt',
             'LOC_city.txt', 'LOC_country.txt', 'LOC_mount.txt', 'LOC_other.txt', 'LOC_state.txt', 'NUM_code.txt',
             'NUM_count.txt', 'NUM_date.txt', 'NUM_dist.txt', 'NUM_money.txt', 'NUM_ord.txt', 'NUM_other.txt',
             'NUM_perc.txt', 'NUM_period.txt', 'NUM_speed.txt', 'NUM_temp.txt', 'NUM_volsize.txt', 'NUM_weight.txt']


def get_dfs(start_path):
    df = pd.DataFrame(columns=['text', 'sent'])
    text = []
    sent = []
    # sent will be the label
    # Loop over pos and neg folder

    for k, filename in enumerate(filenames):
        path = os.path.join(start_path, filename)

        with open(path, "r", encoding='utf8') as myfile:
            # replace carriage return linefeed with spaces
            for line in myfile:
                # print("===", myfile.read())
                text.append(line)
                # label = re.sub(r'.txt', '', filename)
                sent.append(k)  # can on ly use number

    df['text'] = text
    df['sent'] = sent
    # print(df)
    # This line shuffles the data so you don't end up with contiguous
    # blocks of positive and negative reviews
    df = df.sample(frac=1).reset_index(drop=True)
    return df


train_df = get_dfs("./data/cogcomp/train_set_categorized/")


# test_df = get_dfs("aclImdb/test/")
# print(train_df)


def create_and_save_model():
    """
    Convert text data to numeric values for Tensorflow
    """

    # set the vocabulary size
    NUM_WORDS = 10000

    SEQ_LEN = 128
    EMBEDDING_SIZE = 128
    BATCH_SIZE = 128
    EPOCHS = 3
    THRESHOLD = 0.5

    # create tokenizer for our data
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=NUM_WORDS, oov_token='<UNK>')
    tokenizer.fit_on_texts(train_df['text'])

    # convert text data to numerical indexes
    train_seqs = tokenizer.texts_to_sequences(train_df['text'])
    # test_seqs = tokenizer.texts_to_sequences(test_df['text'])

    # Max words to use for each review
    SEQ_LEN = 256
    # pad data up to SEQ_LEN (note that we truncate if there are more than SEQ_LEN tokens)
    train_seqs = tf.keras.preprocessing.sequence.pad_sequences(train_seqs, maxlen=SEQ_LEN, padding="post")

    """
    Build and train model 
    """

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(NUM_WORDS, EMBEDDING_SIZE),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(1, activation='sigmoid')])

    model.summary()

    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])

    # stop training if accuracy start to decrease
    es = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', mode='max')
    callbacks = [es]
    history = model.fit(train_seqs, train_df['sent'].values
                        , batch_size=BATCH_SIZE
                        , epochs=EPOCHS)

    """
    Save the model
    """
    import pickle
    model.save('labels.model')
    # saving
    with open('labels_model.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    del model
    del tokenizer



"""
Prediction usage
"""

NUM_WORDS = 8000
SEQ_LEN = 128
EMBEDDING_SIZE = 128
BATCH_SIZE = 128
EPOCHS = 5
THRESHOLD = 0.5

loaded_model = tf.keras.models.load_model('labels.model')

with open('labels_model.pickle', 'rb') as f:
    loaded_tokenizer = pickle.load(f)

def prepare_predict_data(tokenizer, reviews):
    seqs = tokenizer.texts_to_sequences(reviews)
    seqs = tf.keras.preprocessing.sequence.pad_sequences(seqs, maxlen=SEQ_LEN, padding="post")
    return seqs


my_reviews = ['What is fever?']

my_seqs = prepare_predict_data(loaded_tokenizer, my_reviews)

preds = loaded_model.predict(my_seqs)
pred_df = pd.DataFrame(columns=['text', 'sent'])
pred_df['text'] = my_reviews
pred_df['sent'] = preds

print(pred_df)
# pred_df['sent'] = pred_df['sent'].apply(lambda x: 'pos' if x > THRESHOLD else 'neg')
# print(pred_df)
