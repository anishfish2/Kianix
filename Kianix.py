# Imports
from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import random
import redis
from texttospeech import *
from live2D import *

def read_database():
    '''
    Function to read the database.
    
    TBD placeholder
    '''
    pass

# Main Streamer Class
class Streamer:

    def __init__(self):
        '''
        Constructor for the Streamer class. 
        
        Parameters:
        info (dict): A dictionary containing the streamer's information. This dictionary should contain the following keys:
            - 'name' (str): The name of the streamer.
            - 'plans' (str): The plans for the streamer's stream.
            - 'functions' (list): A list of functions that the streamer can perform.
            - 'time_last_awoken' (float): The time that the streamer was last awoken.
            - 'previously_spoken' (list): A list of the streamer's previous statements.
            - 'previously_responded' (list): A list of chats the streamer has responded to.
            - 'keynotes' (list): A list of keynotes about the streamer.
            ...
        '''
        self.info = {
            'name': 'Kianix',
            'plans': self.read_database('plans'),
            'functions': self.read_database('functions'),
            'time_last_awoken': None,
            'previously_spoken': [],
            'previously_responded': [],
            'keynotes': self.read_database('keynotes')
        }

        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    def __init__(self, info):
        self.info = info
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def awaken(self):
        '''
        Function to awaken Streamer and start stream. Includes main loop during which streamer will 
        continue to make decisions and actions.
        '''
        self.info['time_last_awoken'] = time.time()
        self.info['said_this_stream'] = []

        self.startStream()

        # Main Loop
        while True:
            try:
                self.action_cycle()

            except Exception as e:
                print(f"Error occurred: {e}")
                break
        
    def action_cycle(self):
        '''
        Streamer makes decisions on what to say, what to respond to, what to comment on etc...
        '''
        
        # Implement decision tree
        pass


    def startStream(self):
        '''
        Initialize the stream. Streamer will greet viewers and introduce themselves as well as discuss plans
        for the stream.
        '''
        prompt = f'''You are a vtuber with these characteristics and backstory: {self.info['keynotes']}. You are restarting your stream. 
        Welcome chatters to your stream. Talk about your plans for the day and the future which are {self.info['plans']}. "No swearing or 
        controversy. You have this set of abilities that are encoded as parameters {self.info['functions']}. If you call a function, you 
        will perform the action that it describes. Each function is separated from its description by a ':' and separated from other 
        functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new 
        line no punctuation.'''
            
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages= [{"role": "user", "content": prompt}]
        )
        
        self.speak(response)

    def speak(self, response):
        '''
        Handle text to speech and Unity Expressions.
        '''

        # Parse response
        total = response['choices'][0]['message']['content']
        response_text = total.split("\n")[0]
        function = total.split("\n")[-1].strip().lower()
        ans = response_text

        # Send Unity Expression
        if function.lower() in ["donothing()","confused():","hearts()", "angry()", "pentablet()", "noheadband()", "blush()", "blankeyes()", "pout()", "writetablet()", "brighteyes()"]:
            send_expression(function)

        # Send TTS
        rate = int(len(ans) * .01)
        playTTS(ans, rate)
 
  
    

#Kianix must be running in Unity
def main():
    awake = True
    while awake:
        try:
            kianix_awake()
        except:
            sayGoodbye()
            break

if __name__ == '__main__':
    main()