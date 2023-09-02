import streamlit as st
import replicate
from PIL import Image

# Create a sidebar for previous messages
with st.sidebar:
    st.title('Chat History')

# Create a container for the chat messages
st.title("🌱 Soil Smart")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """
    We are here to help you test your soil fertility, get crop recommendations for that soil,
    as well as discover farming practices that can improve your soil quality over time. We'll guide you on sustainable 
    methods to enhance your soil's health and productivity. simply 
    upload images of your soil or type your question below to get started"""}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

uploaded_image = st.file_uploader("You can Upload an image of your farm soil, to get fertility analysis",
                                      type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)


