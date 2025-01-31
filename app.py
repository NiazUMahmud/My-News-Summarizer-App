import streamlit as st
from transformers import pipeline

def main():
    # Set page layout
    st.set_page_config(
        page_title="News Article Summarizer",
        layout="centered",
        initial_sidebar_state="auto"
    )
    
    # Create a title and description
    st.title("📰 News Article Summarizer")
    st.subheader("Summarize weekly news from renowned English dailies!")

    st.write("""
    **Usage**:
    1. Paste the content (or a chunk) of a news article below.
    2. Click on **Summarize**.
    3. The summarized output will appear below.
    """)

    # Provide a text input area
    article_text = st.text_area(
        "Enter or paste your weekly news article(s) here:",
        height=300
    )

    # Create a button to summarize
    if st.button("Summarize"):
        if article_text.strip() == "":
            st.warning("Please input some text before summarizing.")
        else:
            with st.spinner("Summarizing..."):
                summary = summarize_article(article_text)
            st.success("Summary:")
            st.write(summary)

def summarize_article(text):
    """
    Summarizes the input text using a pre-trained model.
    """
    # Initialize the pipeline
    # Note: Loading a model each time can be slow, so you might want to cache or load once outside the function.
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # The summarizer returns a list of summaries
    summary_list = summarizer(text, max_length=130, min_length=30, do_sample=False)
    
    # Extract the summary text from the first summary result
    summary_text = summary_list[0]['summary_text']
    return summary_text

if __name__ == "__main__":
    main()
