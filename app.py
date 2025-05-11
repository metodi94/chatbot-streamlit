import openai
import streamlit as st
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración básica de la página
st.set_page_config(page_title="ChatBot Interactivo", page_icon="🤖")

# Título de la aplicación
st.title("🤖 Chatbot")

st.write('Bienvenido a la aplicación de chatBot, preguntame lo que necesites.')

# Inicializar el historial de mensajes si no existe
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def get_response(user_message):
    st.session_state['chat_history'].append({'role': 'user', 'content': user_message})
    with st.chat_message('user'):
        st.markdown(user_message)

    response_buffer = ""
    messages = [{'role': msg['role'], 'content': msg['content']} for msg in st.session_state['chat_history']]

    with st.chat_message('assistant'):
        response_placeholder = st.empty()

        try:
            stream = openai.ChatCompletion.create(
                model="o1-mini",
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                if chunk['choices'][0]['delta'].get('content'):
                    response_buffer += chunk['choices'][0]['delta']['content']
                    response_placeholder.markdown(response_buffer)
        except Exception as e:
            response_placeholder.markdown(f"Error al comunicarse con el modelo: {e}")
    
    st.session_state['chat_history'].append({'role': 'assistant', 'content': response_buffer})

# Mostrar el historial del chat si existe
if st.session_state['chat_history']:
    for message in st.session_state['chat_history']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# Entrada de texto para el usuario
if prompt := st.chat_input("Escribe tu pregunta aquí:"):
    get_response(prompt)
