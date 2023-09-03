import os
import streamlit as st
import replicate
from PIL import Image
import cv2
import numpy as np

# App title
st.set_page_config(page_title="🌱 Soil Smart")

# Access the Replicate API token from secrets.toml
replicate_api_token = st.secrets.get("replicate", {}).get("REPLICATE_API_TOKEN", "")

# Check if the API token is empty or not valid
if not replicate_api_token or not (replicate_api_token.startswith('r8_') and len(replicate_api_token) == 40):
    st.warning('Please enter valid credentials in your secrets.toml!', icon='⚠️')
else:
    st.success('Authenticated with Replicate API!', icon='✅')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api_token

st.title("🌱 Soil Smart")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": """
    I'm are here to help you test your soil fertility, get crop recommendations for that soil,
    as well as discover farming practices that can improve your soil quality over time. We'll guide you on sustainable
    methods to enhance your soil's health and productivity. simply
    upload images of your soil or type your question below to get started"""}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": """
    I'm are here to help you test your soil fertility, get crop recommendations for that soil,
    as well as discover farming practices that can improve your soil quality over time. We'll guide you on sustainable
    methods to enhance your soil's health and productivity. simply
    upload images of your soil or type your question below to get started"""}]


st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": 0.75, "top_p": 1, "max_length": 500, "repetition_penalty": 1})
    return output


# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api_token):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


# Function to analyze soil image
def analyze_soil_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the average pixel intensity
    avg_intensity = np.mean(gray)

    # Perform color analysis (e.g., detect brown soil)
    lower_brown = np.array([10, 50, 50])
    upper_brown = np.array([30, 255, 255])
    mask = cv2.inRange(image, lower_brown, upper_brown)
    brown_percentage = (np.count_nonzero(mask) / mask.size) * 100

    return avg_intensity, brown_percentage


uploaded_image = st.file_uploader("You can Upload an image of your farm soil, to get fertility analysis",
                                      type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption=" Soil Image", width=100)

    # Process the uploaded image
    try:
        image = Image.open(uploaded_image)
        image_path = "temp_image.jpg"
        image.save(image_path)

        avg_intensity, brown_percentage = analyze_soil_image(image_path)

        # Display the results
        st.subheader("Analysis Results:")
        st.write(f"Average Pixel Intensity: {avg_intensity:.2f}")
        st.write(f"Percentage of Brown Soil: {brown_percentage:.2f}%")

    except Exception as e:
        st.error(f"Error analyzing soil: {e}")
