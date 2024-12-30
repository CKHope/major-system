import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Function to load images from URLs with caching
@st.cache_data
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

        # Step 2: User input for rows to display
        row_input = st.text_input("Enter row numbers to display (comma-separated, e.g., 33,43):")
        
        if row_input:
            try:
                # Parse the input and convert to a list of integers
                selected_rows = [int(num.strip()) - 1 for num in row_input.split(',')]
            except ValueError:
                st.error("Please enter valid row numbers.")
                return

            # Validate selected rows against the DataFrame length
            selected_rows = [row for row in selected_rows if 0 <= row < len(df)]

            if not selected_rows:
                st.warning("No valid rows selected.")
                return
            
            # Step 3: Display images for selected rows across all columns
            image_links = df['link'].tolist()
            
            cols = st.columns(10)  # Create a grid layout with 10 columns
            
            for row in selected_rows:  # Loop through each selected row
                for col_index in range(10):  # Loop through each of the 10 columns
                    index = row + col_index * len(df) // 10  # Calculate index based on column position
                    
                    if index < len(image_links):
                        image = load_image(image_links[index])
                        if image is not None:
                            # Resize image for faster loading (optional)
                            image.thumbnail((150, 150))  # Resize to thumbnail size (150x150)
                            with cols[col_index]:
                                st.image(image, caption=f"Image {index + 1}", use_container_width=True)

if __name__ == "__main__":
    main()
