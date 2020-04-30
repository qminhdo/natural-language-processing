## NEIU NLP Question Answering Project - Disease and Medication

#### Requirements
Python 3.7
```
# install python 3.7
sudo apt-get update
sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
sudo ap-get install python3.7

# install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py

# install nltk and scikit-learn
python3.7 -m pip install nltk==3.5
python3.7 -m pip install -U scikit-learn==0.22.2

# install zip and unzip
sudo apt install zip unzip

# unzip the data folder 

```
External Packages used in the QA:
- nltk==3.5
- scikit-learn==0.22.2


#### Usage 
Run in terminal, using Python 3.7:
 
```
sudo python3.7 main.py
```

If unable to run, try again with sudo, ntlk has to download corpus and extra priviledge might be required.

Otherwise,install ALL correct packages version using this command:
```
pip install -r requirement.txt
```

#### Author
Quang Minh Do

Some question can take a while to process:
For example: "Can ADHD cause depression?"
This question will cause the QA to look through all file to process
While this question "What is fever" is faster to process because the query keyword is part of a filename
If it is not part of a filename, the system has to open and evaluate all files

#### Data
The data used for this project are scrap using Beautifulsoup4 
from https://www.mayoclinic.org/ and https://www.drugs.com/
 
Data are store in "./data/assorted" directory.
- Disease information (symptoms, causes, treatment, diagnosis)
- Drug information (precaution, direction, help)

Additional data scraped from http://webmd.com/ but not used yet are all the dismed related questions:
Stored in "./data/cogcomp/ENTY_dismed.txt"

#### Project pipeline:
Question is load into QuestionClassier

QuestionClassifier determine the question type and answer type e.g "ENTY:dismed" and other attributes. 
(Details in the file question_classifier.py)

the QuestionClassfier instance is passed into QueryFormulator. 
Here, the queries are built to recieve correct documents

PassageRetriever obtain QuestionClassifier isntance and queries.

The relevant documents that contain such queries are read and segment into passages.

Passages are then score against heuristic and store in an ordered list

The candidate passages are apssed into AnswerProcessor.

The AnswerProcessor lightly format the top 2 answers and retrieve via a method.



