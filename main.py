import gradio as gr
import openai
import pyttsx3
import speech_recognition as sr
import webbrowser as wb

openai.api_key = open('key.txt','r').read().strip('\n')
messages_history = []

voice_assistant = pyttsx3.init()
voice = voice_assistant.getProperty('voices')
voice_assistant.setProperty('voice',voice[1].id)

def speak(audio):
    voice_assistant.say(audio)
    voice_assistant.runAndWait()

def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2
        audio = c.listen(source)
    try:
        query = c.recognize_google(audio,language='en')
        return query
    except sr.UnknownValueError:
        print("Please repeat or typing the command")
print('your command')
text = command()
print(text)
# while True:
# print(sr.Microphone.list_microphone_names())
    # print('what your command')
    # query = command().lower()
    # print(query)

def predict(inp):
    messages_history.append({'role':'user','content':inp})
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages_history,
    #     truyen messages_history de giup kha nang tu hoc cua chatGPT bot
    )
    reply_content = completion.choices[0].message.content
    # print(reply_content)
    messages_history.append({'role':'assistant','content':reply_content})
    response = [(messages_history[i]['content'],messages_history[i+1]['content']) for i in range(0,len(messages_history),2)]
    return response
# for i in range(2):
#     user_input = input(">:")
#     print(user_input)
#     print(chat(user_input))
# with gr.Blocks() as demo:
#     chatbot = gr.Chatbot()
#     with gr.Row():
#         txt = gr.Textbox(show_label=False,placeholder='Type your message here').style(container=False)
#         txt.submit(predict,txt,chatbot)
#         txt.submit(lambda: "",None,txt)
#         txt.submit(None,None,txt,_js="() => {''}")
#
# demo.launch(share=True)
