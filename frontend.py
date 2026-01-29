import streamlit as st
from backend import workflow,retrive_thread
from langchain_core.messages import HumanMessage
import uuid

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id']) 
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return workflow.get_state(config = {'configurable':{'thread_id':thread_id}}).values.get('messages',[])

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_thread()

add_thread(st.session_state['thread_id'])

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversation')
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        tmp = []
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            tmp.append({'role':role,'content':msg.content})
        st.session_state['message_history'] = tmp


for i in st.session_state['message_history']:
    with st.chat_message(i['role']):
        st.markdown(i['content'])
         
user_input = st.chat_input('Typr here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    config = {'configurable':{'thread_id':st.session_state['thread_id']}}
    #result = workflow.stream({'messages':HumanMessage(content=user_input)},
    #                         config,stream_mode='messages')
    #for message_chunk,metadata in result:
    #    st.session_state['message_history'].append({'role':'assistant','content':message_chunk.content})
    #    with st.chat_message('assistant'):
    #        st.markdown(message_chunk.content)
        
    #ai_response = result['messages'][-1].content
    

    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            message_chunk for message_chunk,metadata in workflow.stream(
                {'messages':HumanMessage(content=user_input)},
                config = config,
                stream_mode = "messages"
            )
        )
        st.session_state['message_history'].append({'role':'assistant','content':ai_response})