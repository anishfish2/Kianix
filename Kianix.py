# Imports
from dotenv import load_dotenv
import time
import os
import openai
import random
from live2D import *
import firebase_admin
from firebase_admin import firestore

# Main Streamer Class
class Streamer:

    def __init__(self, info=None):
        '''
        Constructor for the Streamer class. 
        
        Parameters:
        info (dict, optional): A dictionary containing the streamer's information. If not provided, default values are used.
            - 'name' (str): The name of the streamer.
            - 'plans' (str): The plans for the streamer's stream.
            - 'functions' (list): A list of functions that the streamer can perform.
            - 'time_last_awoken' (float): The time that the streamer was last awoken.
            - 'previously_spoken' (list): A list of the streamer's previous statements.
            - 'previously_responded' (list): A list of chats the streamer has responded to.
            - 'keynotes' (list): A list of keynotes about the streamer.
            ...
        '''
        app = firebase_admin.initialize_app(options={'projectId' :'kianix'})
        self.db = firestore.client(app)

        # If info is not provided, use default values
        if info is None:
            self.info = {
                'name': 'Kianix',
                'time_last_awoken': None,
                'previously_spoken': [],
                'previously_responded': [],\
            }
        else:
            self.info = info

        self.info['plans'] = self.read_database('Plans')
        self.info['keynotes'] = self.read_database('Keynotes')
        self.info['functions'] = self.read_database('Functions')

        chat_log = self.read_database('Functions')
        self.info['latest_respondec_index'] = self.read_database('Functions')

        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def read_database(self, field=None):
        '''
        Function to read the database for the streamer's information.
        '''
        doc_ref = self.db.collection('streamers').document(self.info['name'])
        doc = doc_ref.get()
        return doc.to_dict().get(field, None)

    def write_database(self, field=None, input=None, update=False):
        '''
        Function to write to the database for the streamer's information.
        '''
        doc_ref = self.db.collection('streamers').document(self.info['name'])
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if update:
                doc_ref.update({
                    field : input
                })
                return
            
            chat_log = data.get(field, [])
            
            # if the input is a list add the list to the chat log
            if isinstance(input, list):
                chat_log += input
            else:
                chat_log.append(input)
            
            doc_ref.update({
                field : chat_log
            })

    def clear_database(self, field=None):
        '''
        Function to clear the database for the streamer's information. Clears based on field type.
        '''
        doc_ref = self.db.collection('streamers').document(self.info['name'])
        doc_ref.update({field: []})

    def awaken(self):
        '''
        Function to awaken Streamer and start stream. Includes main loop during which streamer will 
        continue to make decisions and actions.
        '''
        self.info['time_last_awoken'] = time.time()
        self.info['said_this_stream'] = []

        self.write_database('awake', True, update=True)
        # self.startStream()

        # Main Loop
        while self.read_database('awake'):
            try:
                self.info['plans'] = self.read_database('plans')
                self.info['keynotes'] = self.read_database('keynotes')
                self.info['functions'] = self.read_database('functions')
                self.action_cycle()

            except Exception as e:
                print(f"Error occurred: {e}")
                # break
            time.sleep(2)
        
    def action_cycle(self):
        '''
        Streamer makes decisions on what to say, what to respond to, what to comment on etc...
        '''
        chat = self.read_chat()

        prompt = f'''You are a vtuber with these characteristics and backstory: {self.info['keynotes']}. Someone wrote this to you in chat.: {chat}. 
        It may contain twitch emojis. Write a response to it. No emojis. ASCII characters only. No swearing or controversy. You have this set of abilities 
        that are encoded as parameters: {self.info['functions']}. If you call a function, you will perform the action that it describes. Each function 
        is separated from its description by a ":" and separated from other functions by a ";" After categorizing your response, simply call one function using 
        its name and '()' and write it after a new line no punctuation.'''
            
        response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages= [{"role": "user", "content": prompt}]
        )

        total = response['choices'][0]['message']['content']
        response_text = total.split("\n")[0]
        function = total.split("\n")[-1].strip().lower()
        ans = response_text
        print(ans)

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
        model="gpt-4o",
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
        print(ans)

        # Send Unity Expression
        # if function.lower() in ["donothing()","confused():","hearts()", "angry()", "pentablet()", "noheadband()", "blush()", "blankeyes()", "pout()", "writetablet()", "brighteyes()"]:
        #     send_expression(function)

        # Send TTS
        # rate = int(len(ans) * .01)
        #playTTS(ans, rate)
 
    def read_chat(self):
        '''
        Read the first unread chat from the database.
        '''

        unread_chat_log = self.read_database('unread_chat_log')
        if len(unread_chat_log) == 0:
            return None
        chat = unread_chat_log.pop(0)
        self.write_database('read_chat_log', chat)
        self.write_database('unread_chat_log', unread_chat_log, update=True)
        return chat
  
def main():
    kianix = Streamer()
    kianix.awaken()
    
if __name__ == '__main__':
    main()