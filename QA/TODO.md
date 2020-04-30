## Development steps

* Greet user, ask user's condition, what question does the user need to be answered
* Ask user question
* Get question type, answer type, queries
* Get relevant documents using queries
* Get candidate passages
* Score passages on some metric
* Select best passage
* Formulate passage into answer
* Response to user
    
## Question Flow

* How are you today?
    * Not good: Ask for more   
        * Determine user's symptom
    * Good: Ask what can I do, what question do you have in mind?
        
## Parse Answer Types

Here are the possible answer types cover by this project:
* Definition
* Description
* Treatment / Prevention
* Symptom
* Binary (yes/no verification)
* Location
* Time

###### Definition:

* What is X
    * X can be:
        * Medicine name, https://www.drugs.com/sfx/aspirin-side-effects.html
        * Symptom: fever, headache, https://www.mayoclinic.org/diseases-conditions/jet-lag/symptoms-causes/syc-20374027 
    * Answer: 
        * X is ...
    
###### Description
Key words:

* What X do I get after Y
    * What test do I get after having fever
    
* What is SIDE EFFECT of X
    * Similar question: What is the RISKS of TAKING X
    * Implementation:
        * Use review source from webmd:
            * Drug list: https://www.webmd.com/drugs/2/index
            * Specific drug review example: https://www.webmd.com/drugs/2/drug-5166-368/ibuprofen-oral/ibuprofen-chewable-oral/details
            
* What do you think of X
###### Location:
    
* Where can I X
    * X can be: 
        * go for taking X-ray
        * do eye exam             
    * Answer:
        * X can be performed at ADDRESS, contact is PHONE_NUMBER   
            
###### Symptom:
key words: 
* symptom of
* cause of

* What is symptom of X
    * X can be: fever, headache    
    * Answer: 
        * Symptom of fever are ...
        
* What is common cause of X

###### Binary
* (Will|do|should) I need X
* (Is|are|do|does|) X

###### Treatment:

* What is the treatment for X
    * X can be: fever, headache
    
###### Location

* Where VB X
* Where (do|can|could|should) I X


###### Time
* When X
* When (do|can|could|should) I X


###### Other type of question
* What if
* How is X similar to Y
* Why do I X
* How (much|many) X
* Who X