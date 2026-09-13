
from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()
client = Anthropic()
model = "claude-sonnet-4-5"

def useHaiku():
    global model
    model = "claude-haiku-4-5"

def addUserMsg(messages, text):
    msg = {"role":"user", "content":text}
    messages.append(msg)

def addAssistantMsg(messages, text):
    msg = {"role":"assistant", "content":text}
    messages.append(msg)

def sendMsg(messages, text, systemPrompt=None, startFrom=None, stop_sequence=None):
    addUserMsg(messages,text)
    if startFrom:
        addAssistantMsg(messages, startFrom)
    params = {
        "model":model,
        "max_tokens":1000,
        "messages":messages,
    }
    if stop_sequence:
        params["stop_sequences"] = [stop_sequence]
    if systemPrompt:
        params["system"] = systemPrompt
    response = client.messages.create(**params)
    respText = response.content[0].text
    addAssistantMsg(messages,respText)
    return respText

def sendStream(messages, text, callback):
    addUserMsg(messages, text)
    with client.messages.stream(
            model=model,
            max_tokens=1000,
            messages=messages
    ) as stream:
        for text in stream.text_stream:
            callback(text)
        return stream.get_final_message().content[0].text

def sendMsgGetJson(messages, text):
    resp = sendMsg([], text, startFrom="```json", stop_sequence="```")
    return json.loads(resp)