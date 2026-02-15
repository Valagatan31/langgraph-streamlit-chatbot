import streamlit as st
from backend import workflow, retrive_thread
from langchain_core.messages import HumanMessage
import uuid

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id']) 
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# Initialize Session States
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_thread()

add_thread(st.session_state['thread_id'])

# Sidebar Logic
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id), key=thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        tmp = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            tmp.append({'role': role, 'content': msg.content})
        st.session_state['message_history'] = tmp
        st.rerun()

# Display Chat History
for i in st.session_state['message_history']:
    with st.chat_message(i['role']):
        st.markdown(i['content'])

# Chat Input
user_input = st.chat_input('Type here...')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    config = {
        'configurable': {'thread_id': st.session_state['thread_id']},
        'run_name': "chat_turn"
    }

    def response_generator():
        # Corrected indentation for the generator
        for message_chunk, metadata in workflow.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            # Check if chunk has content and extract text only
            if hasattr(message_chunk, "content"):
                content = message_chunk.content
                
                if isinstance(content, str) and content:
                    yield content
                
                elif isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict) and "text" in part:
                            yield part["text"]
                        elif isinstance(part, str):
                            yield part

    with st.chat_message("assistant"):
        # This will now display clean text without the JSON fragments
        ai_response = st.write_stream(response_generator())

    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_response
    })