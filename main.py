import re
import os
from twilio.twiml import messaging_response
import long_responses as long
from twilio.rest import Client
from flask import Flask,request,redirect
from twilio.twiml.messaging_response import MessagingResponse
        

def decline_questionare(val):
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
            split_message = str(user_input)
            split_message1 = re.split(r'\s+|[,;?!.-]\s*', split_message.lower())
            response = check_all_messages(split_message)
            return response


        MessagingResponse().message(get_response(val))


account_sid = "ACcce2a2ed0cf279a084305106d69b4488"
# example my sid = "ACcce2a2ed0cf279a084305106d69b4488" Dont share this is private
auth_token = "eabf7c9c3ab59bc50558d1e0f115ddf7"
# example my auth_token = "263c8923725accab29a7184f7b1b84ed" Dont share this is private
client = Client(account_sid,auth_token)
first_responce = "Hello! I am flash. I am a chatbot who can help you conquer your loneliness by using advanced AI and machine learning algorithms.Can i ask some questions to improve my conversation with you and get a better knowledge of your interests? "
# first_responce = "Hello"
def send_message(msg):
    client.messages.create(
        to="",
        from_="+14752566126",
        body=msg
    )
send_message(first_responce)

app = Flask(__name__)

@app.route("/sms",methods=['GET','POST'])

def main_app():
    body = request.values.get('Body',None)
    resp = MessagingResponse()
    string1 = str(body)
    print(string1.lower)
    if string1.lower() == "yes" or string1.lower() == "yea":
        questions = ["What is your name?","What is your age","what are your interests?","Do u have a job?"]
        file_open2 = open("answers.txt",'a')
        session = True
        for i in range(0,len(questions)):
            send_message("What is your name?")
            body = request.values.get('Body',None)
            resp = MessagingResponse()
            resp.message("Nice to meet you {}")
            resp.message("Would you like to share with me some of your interests or hobbies?(Tell me up to 5 favorite things you enjoy doing in your free time.)")
            body = request.values.get('Body',None)
            file_open2.write(str(body)+"\n")
    else:
        no_questionare = "So if u dont want the questionare , well then we can continue normal chatting. So tell me about your interests? Just kidding, you can start the conversation now."
        resp.message(no_questionare)
        resp = MessagingResponse()
        response_value = request.values.get('Body',None)
        decline_questionare(response_value)

        
    return str(resp)

if __name__=="__main__":
    app.run(debug=True)
