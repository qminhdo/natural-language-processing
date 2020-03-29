n_trigrams = __import__("n-trigrams")

######################
# Testing
input_filename = "sample3.txt"
model_filename = "sample3.txt.model"
ntrigram = n_trigrams.NTrigram(input_filename, model_filename)
ntrigram.save_model_to_file()