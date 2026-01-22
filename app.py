# main file to run the MindTree application
import streamlit as st


def main():
    """Main function to run the MindTree application."""
    st.set_page_config(
        page_title="MindTree",
        page_icon="🌳",
        layout="wide"
    )
    
    st.title("🌳 MindTree")
    st.write("Welcome to MindTree - A tree making application")
    
    # Placeholder for future functionality
    st.info("This application is under development.")


if __name__ == "__main__":
    main()
