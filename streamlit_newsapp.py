import os
import streamlit as st
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- Helper Functions ---
def setup_newsapi():
    """Initialize NewsAPI client using the News API key."""
    if not NEWS_API_KEY:
        st.error("NewsAPI key missing! Add to .env file or environment variables.")
        return None

    try:
        return NewsApiClient(api_key=NEWS_API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize NewsApiClient: {str(e)}")
        return None


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

def get_news_sources(newsapi_client):
    """Fetch available news sources from the News API."""
    try:
        sources_data = newsapi_client.get_sources()
        if sources_data and sources_data['status'] == 'ok':
            sources = sources_data['sources']
            # Return a list of tuples: (source name, source id)
            return [(source['name'], source['id']) for source in sources]
        else:
            st.error("Failed to retrieve news sources.")
            return []
    except Exception as e:
        st.error(f"Error fetching news sources: {str(e)}")
        return []


# --- Streamlit UI ---
st.set_page_config(
    page_title="Cloud News Summarizer",
    page_icon="🌩️",
    layout="centered"
)


def main():
    st.sidebar.title("Configuration")

    newsapi_client = setup_newsapi()
    if not newsapi_client:
        return

    # Fetch news sources and populate the select box
    available_sources = get_news_sources(newsapi_client)
    if not available_sources:
        return  # Exit if no sources are available

    source_names, source_ids = zip(*available_sources)  # Unpack into separate lists

    # News source selection
    selected_source_name = st.sidebar.selectbox(
        "Select News Source",
        source_names,  # Display names
        index=source_names.index("BBC News") if "BBC News" in source_names else 0 # Default to BBC if available
    )
    selected_source_id = source_ids[source_names.index(selected_source_name)] # Get the ID

    # Date selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=[start_date, end_date],
        max_value=end_date
    )


    # Main interface
    st.title("🌩️ Cloud-based News Summarizer")
    st.markdown("Summarizes news articles using **OpenAI**—no local models required!")


    if st.sidebar.button("🚀 Fetch & Summarize"):
        # Validate date range selection
        if len(selected_dates) != 2:
            st.warning("Please select a valid date range.")
            return

        with st.spinner("Searching for news articles..."):
            try:
                articles_data = newsapi_client.get_everything(
                    sources=selected_source_id,
                    from_param=selected_dates[0],
                    to=selected_dates[1],
                    language='en',
                    sort_by='relevancy',
                    page_size=30  # Reduced for API usage safety
                )
            except Exception as e:
                st.error(f"Error fetching articles: {str(e)}")
                articles_data = None # ensure it's None to prevent further processing

            if articles_data and articles_data['status'] == 'ok':
                articles = articles_data['articles']
            else:
                 articles = []

        if not articles:
            st.warning(f"No articles found for source: {selected_source_name}.")
            return

        st.success(f"Found {len(articles)} articles from {selected_source_name}")
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

                        # Summarize the article immediately and display
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