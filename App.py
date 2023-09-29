import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

# Initialize the session state
if "generated" not in st.session_state:
    st.session_state["generated"] = [] # output
if "past" not in st.session_state:
    st.session_state["past"] = [] # past
if "input" not in st.session_state:
    st.session_state["input"] = "" # input
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = [] # stored_session

# define function to get user input
def get_text():
    """ 
    Get user input from text_input widget
    Returns:
        str: user input
    """
    input_text = st.text_input("You: ", st.session_state["input"],
                               placeholder="Your AI assistant is ready to help you!",
                               label_visibility="hidden")
    return input_text

st.title("AI Assistant")

# API 
api = st.sidebar.text_input("API Key", type = "password")
MODEL = st.sidebar.selectbox(label= "Model", options = ["gpt-3.5-turbo", "gpt-3.5", "gpt-3", "gpt-2", "gpt-2-xl"])

if api:
    
    # Create a OpenAI instance
    llm = OpenAI(
        temperature=0,
        openai_api_key=api,
        model_name = MODEL
    )

    # Create a Conversation memory
    if "entity_memory" not in st.session_state:
        st.session_state["entity_memory"] = ConversationEntityMemory(llm = llm, k = 10)
    
    # Create the conversation chain
    Conversation = ConversationChain(
        llm = llm,
        prompt = ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory = st.session_state["entity_memory"]
        
    )
else:
    st.error("Please enter your API key")
    
# Get user input
user_input = get_text()

# Generate the output using the conversation chain object and the user input

if user_input:
    output = Conversation.run(input = user_input)
    
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    
with st.expander("Conversation"):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.write("You: ", st.session_state['past'][i])
        st.write("AI: ", st.session_state['generated'][i])
        st.write("---")

        