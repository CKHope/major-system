import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Function to load images from URLs with caching
# @st.cache_data
def load_image(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        st.error(f"Error loading image from {url}: {e}")
        return None

# Streamlit app
def main():
    st.title("Image Display from Excel")

    # Step 1: Upload Excel file
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Ensure the DataFrame has the expected structure
        if 'link' not in df.columns:
            st.error("The uploaded Excel file must contain a column named 'link'.")
            return

        # Step 2: Display images in a grid format
        image_links = df['link'].tolist()
        
        # Create a grid layout with 10 columns for each range of images
        cols = st.columns(10)
        
        for i in range(10):  # Loop through each of the 10 columns
            with cols[i]:
                for j in range(100):  # Each column will have up to 100 images
                    index = i * 100 + j  # Calculate the correct index for the image link
                    if index < len(image_links):
                        image = load_image(image_links[index])
                        if image is not None:
                            # Resize image for faster loading (optional)
                            image.thumbnail((150, 150))  # Resize to thumbnail size (150x150)
                            st.image(image, caption=f"Image {index + 1}", use_column_width=True)

if __name__ == "__main__":
    main()
