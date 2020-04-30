import sys, re
import nltk
import random

class Agent:
    def __init__(self):
        self.agent_responses = {}
        questions_stack = []
        answers_stack = []
        info_gathered = {}
        user_detail = {"gender": "NA", "age": "NA", "weight": "NA"}

        self.setup_agent_responses()

    def start_conversation(self, questions_flow):
        ans = self.ask_question("Hello, how are you today?")
        self.response_random(self.agent_responses.get("bad_condition_affirm"))
        self.response_random(self.agent_responses.get("bye"))


    def response(self, data, response_type = "terminal"):
        """
        Display data to selected screen type
        :param data: (String) the data to display to screen
        :param response_type: (String) screen type, default: terminal
        """
        if (response_type == "terminal"):
            print(data, end="\n")

    def response_random(self, data, response_type = "terminal"):
        if(response_type == "terminal"):
            res = random.choice(data)
            self.response(res)

    def setup_agent_responses(self):
        self.agent_responses.update({
            "wait": [
                "Please wait while I gather that information for you",
                "Please wait for a moment",
                "I will be back with you in a moment",
                "Please hold"
            ],
            "affirm": [
                "Thank you!",
                "Got it!"
            ],
            "good_condition_affirm": [
                "Wonderful!",
                "Glad to hear that"
            ],
            "bad_condition_affirm": [
                "Sorry to hear that",
                "That must be awful"
            ],
            "bye": [
                "See you again!",
                "Goodbye!"
            ],
            "confuse": [
                "I'm not quite understand it, can you please repeat it",
                "Not sure if I'm understanding you correctly, please elaborate"
            ]
        })

    def ask_question(self, question):
        """
        Ask the user question and request an input from user
        :param (String) question: the input question
        :return (String): input from user
        """
        self.response((question))
        return input()

