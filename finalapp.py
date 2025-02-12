# news_summarizer_api.py
import os
import streamlit as st
from datetime import datetime, timedelta
#from newsapi import NewsApiClient # try to remove this import for now
import newsapi  # Add newsapi to verify the package exists
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def setup_newsapi():
    """Initialize NewsAPI client using the News API key."""
    if not NEWS_API_KEY:
        st.error("NewsAPI key missing! Add to .env file or environment variables.")
        return None
    # Check if NewsApiClient exists with dir(newsapi). We will try this out later.
    print(f"Classes in newsapi: {dir(newsapi)}") # Print the classes available in the library

    #if "NewsApiClient" in dir(newsapi): # We will try this out later
    #     return newsapi.NewsApiClient(api_key=NEWS_API_KEY) # We will try this out later
    #else: # We will try this out later
    #      st.error("NewsApiClient not found, check your newsapi version") # We will try this out later
    #      return None  # We will try this out later
    return # Temporary test return

def summarize_with_openai(text):
    """Use LangChain ChatOpenAI to summarize articles in 3 sentences."""
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage

    if not OPENAI_API_KEY:
        st.error("OpenAI API key missing! Add to .env file or environment variables.")
        return None

    try:
        chat = ChatOpenAI(
            temperature=0.5,
            openai_api_key=OPENAI_API_KEY  # Ensure the key is passed here
        )
        message = HumanMessage(content=f"Summarize this news article in 3 sentences:\n\n{text}")
        response = chat([message])
        return response.content.strip()
    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="Cloud News Summarizer",
    page_icon="🌩️",
    layout="centered"
)

def main():
    st.sidebar.title("Configuration")

    # Date selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=[start_date, end_date],
        max_value=end_date
    )

    # News source input
    news_source = st.sidebar.text_input(
        "News Source ID",
        value="bbc-news",
        help="Find sources at https://newsapi.org/sources"
    )

    # Main interface
    st.title("🌩️ Cloud-based News Summarizer")
    st.markdown("Summarizes news articles using **OpenAI**—no local models required!")

    newsapi = setup_newsapi()
    if not newsapi:
        return

    if st.sidebar.button("🚀 Fetch & Summarize"):
        # Validate date range selection
        if len(selected_dates) != 2:
            st.warning("Please select a valid date range.")
            return

        with st.spinner("Searching for news articles..."):
            # Temporary removal of newsapi call for debugging
           # articles_data = newsapi.get_everything(
           #     sources=news_source,
           #     from_param=selected_dates[0],
           #     to=selected_dates[1],
           #     language='en',
           #     sort_by='relevancy',
           #     page_size=30  # Reduced for API usage safety
           # )
           articles_data = [] # Temporary to fix code,

        articles = articles_data['articles'] if articles_data else []

        if not articles:
            st.warning("No articles found.")
            return

        st.success(f"Found {len(articles)} articles")
        st.divider()

        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Untitled')
            content = article.get('content', '')

            with st.expander(f"{idx}. {title}", expanded=False):
                col1, col2 = st.columns([0.7, 0.3])

                with col1:
                    if content:
                        # Strip extraneous text from NewsAPI content, e.g. " [ +999 chars]"
                        clean_content = content.split(' [')[0]

                        st.markdown("#### Original Content")
                        st.write(clean_content[:1000] + "...")  # Show first 1000 chars

                        if st.button("Generate Summary", key=f"summarize_{idx}"):
                            with st.spinner("Summarizing..."):
                                summary = summarize_with_openai(clean_content)

                                if summary:
                                    st.markdown("#### AI Summary")
                                    st.success(summary)
                                else:
                                    st.error("Failed to generate summary.")
                    else:
                        st.write("No content available.")

                with col2:
                    url_to_image = article.get('urlToImage')
                    if url_to_image:
                        st.image(
                            url_to_image,
                            caption=article['source']['name'],
                            use_container_width=True
                        )
                    st.markdown(f"[📖 Full Article]({article.get('url', '')})")
                    published_at = article.get('publishedAt', '')[:10]
                    if published_at:
                        st.caption(f"Published: {published_at}")

if __name__ == "__main__":
    main()