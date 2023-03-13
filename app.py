import openai
import streamlit as st
from streamlit_chat import message
openai.api_key = "YOUR_API_KEY_HERE"

def generate_response(prompt, engine, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    completion=openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    message=completion.choices[0].text
    return message

def main():
    # Set page title
    st.title("ChatGPT Web App Par Sayon")

    # Set up sidebar options
    engine_options = {
        "Davinci": {
            "Text": "text-davinci-003",
            "Code": "code-davinci-002"
        }
    }

    # Set up initial settings
    settings = {
        "engine": "Davinci",
        "mode": "Text",
        "temperature": 0.7,
        "max_tokens": 190,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    # get user API key
    api_key = st.text_input("Entrez votre clé OpenAI API Key:", type="password")

    if api_key:
        openai.api_key = api_key

       
        
        
        # storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []

        user_input=st.text_input("You:",key='input')

        if user_input:
            message(user_input, is_user=True)
            prompt = "\n".join([f"You: {msg}" for msg in st.session_state["past"]] + [f"Bot: {user_input}"])
            engine = engine_options[settings["engine"]][settings["mode"]]
            output=generate_response(prompt, engine, settings["temperature"], settings["max_tokens"], settings["top_p"], settings["frequency_penalty"], settings["presence_penalty"])
            #message(output)

            #store the output
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

        if st.session_state['generated']:

            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                
        # Display chat settings sidebar
        st.sidebar.title("Paramètres")
        settings["engine"] = st.sidebar.selectbox("Engine", list(engine_options.keys()))
        settings["mode"] = st.sidebar.selectbox("Mode", list(engine_options[settings["engine"]].keys()))
        settings["temperature"] = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, value=settings["temperature"])
        settings["max_tokens"] = st.sidebar.slider("Max Tokens", min_value=1, max_value=2048, step=1, value=settings["max_tokens"])
        settings["top_p"] = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, step=0.1, value=settings["top_p"])
        settings["frequency_penalty"] = st.sidebar.slider("Frequency Penalty", min_value=0.0, max_value=1.0, step=0.1, value=settings["frequency_penalty"])
        settings["presence_penalty"] = st.sidebar.slider("Presence Penalty", min_value=0.0, max_value=1.0, step=0.1, value=settings["presence_penalty"])
                                                              # Display current settings
        st.sidebar.markdown("### Paramètres Actuels")
        st.sidebar.write(f"Engine: {settings['engine']}")
        st.sidebar.write(f"Mode: {settings['mode']}")
        st.sidebar.write(f"Temperature: {settings['temperature']}")
        st.sidebar.write(f"Max Tokens: {settings['max_tokens']}")
        st.sidebar.write(f"Top P: {settings['top_p']}")
        st.sidebar.write(f"Frequency Penalty: {settings['frequency_penalty']}")
        st.sidebar.write(f"Presence Penalty: {settings['presence_penalty']}")        

if __name__ == '__main__':
    main()
