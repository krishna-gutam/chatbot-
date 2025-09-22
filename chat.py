import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot with Memory", page_icon=":brain:")
st.title("Chatbot with Memory")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]

# Get Google API Key from user
api_key = st.text_input("Enter your Google API Key:", type="password")

if api_key:
    try:
        # Initialize the model
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

        # Display chat messages from history on app rerun
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)

        # React to user input
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            st.chat_message("Human").write(prompt)

            # Add user message to chat history
            st.session_state.chat_history.append(HumanMessage(content=prompt))

            with st.spinner("Thinking..."):
                # Get AI response
                response = model.invoke(st.session_state.chat_history)

                # Display AI response in chat message container
                st.chat_message("AI").write(response.content)

                # Add AI response to chat history
                st.session_state.chat_history.append(AIMessage(content=response.content))

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check your API key and try again.")

else:
    st.info("Please enter your Google API Key to start chatting.")
