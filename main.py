import re
from twilio.twiml import messaging_response
import long_responses as long
from twilio.rest import Client
from flask import Flask,request,redirect
from twilio.twiml.messaging_response import MessagingResponse


account_sid = "ACcce2a2ed0cf279a084305106d69b4488"
# example my sid = "ACcce2a2ed0cf279a084305106d69b4488" Dont share this is private
auth_token = "263c8923725accab29a7184f7b1b84ed"
# example my auth_token = "263c8923725accab29a7184f7b1b84ed" Dont share this is private
client = Client(account_sid,auth_token)
first_responce = "Hello! I am flash.I am a chatbot who can help you conquer your loneliness by using advanced AI and machine learning algorithms.Can i ask some questions to improve my conversation with you and get a better knowledge of your interests? "

def send_message(msg):
    client.messages.create(
        to="+372 56660340",
        from_="+14752566126",
        body=msg
    )
app = Flask(__name__)

@app.route("/sms",methods=['GET','POST'])
def choice():
    ok_resp = ["ok","yea","yes","i will","hmm"]
    resp = messaging_response()
    if str(resp).lower() == [i for i in ok_resp]:
        accept_questionare()
    else:
        decline_questionare()
    pass

def accept_questionare():
    file_open = open("questionare.txt",'r')
    file_open2 = open("answers.txt",'a')
    questions = file_open.readlines() 
    for i in range(0,len(questions)):
        send_message(questions[i])
        resp = messaging_response()
        file_open2.write(str(resp)+"\n")

def decline_questionare():
    def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
        message_certainty = 0
        has_required_words = True

        # Counts how many words are present in each predefined message
        for word in user_message:
            if word in recognised_words:
                message_certainty += 1

        # Calculates the percent of recognised words in a user message
        percentage = float(message_certainty) / float(len(recognised_words))

        # Checks that the required words are in the string
        for word in required_words:
            if word not in user_message:
                has_required_words = False
                break

        # Must either have the required words, or be a single response
        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0


    def check_all_messages(message):
        highest_prob_list = {}

        # Simplifies response creation / adds it to the dict
        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob_list
            highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
        
        # Responses -------------------------------------------------------------------------------------------------------
        response("hello", ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
        response('See you!', ['bye', 'goodbye'], single_response=True)
        response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
        response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
        response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

        # Longer responses
        response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
        response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

        best_match = max(highest_prob_list, key=highest_prob_list.get)
        # print(highest_prob_list)
        # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

        return long.unknown() if highest_prob_list[best_match] < 1 else best_match


    # Used to get the response
    def get_response(user_input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        response = check_all_messages(split_message)
        return response


    # Testing the response system
    while True:
        messaging_response().message(get_response(messaging_response))
