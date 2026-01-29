from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List,Annotated
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage
import sqlite3

llm = ChatGoogleGenerativeAI(
    model='models/gemini-flash-latest',
    google_api_key='AIzaSyCKJR9lB1W3pNp_jB_90psmJemylQzSuPo',
    temperature=0.7
)

class ChatState(TypedDict):
    messages:Annotated[List[str],add_messages]

graph = StateGraph(ChatState)

def generate_answer(state: ChatState):
    response = llm.invoke(state['messages'])
    return {'messages':[response]}
    
graph.add_node('generate_answer',generate_answer)

graph.add_edge(START,'generate_answer')
graph.add_edge('generate_answer',END)

conn = sqlite3.connect(database = 'chatbot3.db',check_same_thread = False)
checkpointer = SqliteSaver(conn = conn)
workflow = graph.compile(checkpointer = checkpointer)

def retrive_thread():
    all_thread = set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])
    return list(all_thread)

#result = workflow.invoke(
#    {'messages':HumanMessage(content='what is my name?')},
#    config = {'configurable':{'thread_id':1}},
#)

#print(result)



