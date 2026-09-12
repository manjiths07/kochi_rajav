import random
import time
import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Feline Fortune Oracle", page_icon="🐈", layout="centered"
)

st.title("🐈 പൂച്ച ജ്യോതിഷി (The Feline Oracle)")
st.write(
    "Upload a cat's photo and let the mystical feline decide your tech & life"
    " fate!"
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose a cat photo...", type=["jpg", "jpeg", "png"]
)

# Gen-Z & Funny Predictions List
predictions = [
    (
        "🚨 കഠിനമായ ദുരന്തം! ഈ പൂച്ചയുടെ നോട്ടം കാണുമ്പോൾ അടുത്ത കോഡിങ്ങിൽ നിനക്ക്"
        " വലിയൊരു സിന്റാക്സ് എറർ വരാൻ പോകുന്നു."
    ),
    (
        "✨ മഹാഭാഗ്യം! പൂച്ച വാലാട്ടി കടന്നുപോയ സ്ഥിതിക്ക് ഇന്ന് നിന്റെ കോഡ് ഒറ്റ"
        " ഇരുപ്പിൽ റൺ ആയി കിട്ടും."
    ),
    (
        "⚠️ Gen-Z ജാഗ്രത! ഇന്ന് നിന്റെ ലാപ്‌ടോപ്പ് ഫാൻ ഒരു ഹെലികോപ്റ്റർ പോലെ"
        " സൗണ്ട് ഉണ്ടാക്കും."
    ),
    (
        "🔮 പ്രണയ ഫലം: ഈ പൂച്ച നിന്നെ മൈൻഡ് ചെയ്യാത്തതുപോലെ, നീ ക്രഷിന്"
        " അയച്ച മെസ്സേജും സീൻ കാണാതെ കിടക്കും."
    ),
    (
        "🔥 ഇന്ന് നിന്റെ കോഡിങ് സ്പീഡ് വേറെ ലെവൽ ആയിരിക്കും, പക്ഷേ കറന്റ്"
        " പോകാൻ ചാൻസ് ഉണ്ട്!"
    ),
]

if uploaded_file is not None:
  # Display the uploaded image
  image = Image.open(uploaded_file)
  st.image(image, caption="The Mystic Cat of the Day", width=300)

  if st.button("🔮 Reveal My Fate (ജാതകം നോക്കൂ)"):
    with st.spinner("Analyzing cat whiskers and mystical vibrations..."):
      # Adding a dramatic delay
      time.sleep(2)

      # Pick a random funny prediction
      result = random.choice(predictions)
      st.success("ആകാശത്തുനിന്നും അശരീരി വന്നു!")
      st.markdown(f"### **{result}**")