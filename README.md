# My-News-Summarizer-App
# 🌩️ Cloud-Based News Summarizer

A Streamlit application that leverages the News API and OpenAI's language models to provide concise summaries of news articles from various sources.


https://github.com/user-attachments/assets/3fd7a027-4098-4db0-aaa7-a5a97285222d


## Table of Contents

*   [Functionality](#functionality)
*   [Tools Used](#tools-used)
*   [Setup](#setup)
*   [Usage](#usage)
*   [Blog Post: The Power of AI-Driven News Summarization](#blog-post-the-power-of-ai-driven-news-summarization)
*   [Contributing](#contributing)
*   [License](#license)

## Functionality

This application allows users to:

*   **Select a news source:** Choose from a dynamic list of available news sources powered by the News API.
*   **Define a date range:** Specify a start and end date to filter articles.
*   **Fetch news articles:** Retrieve a list of articles based on the selected source and date range.
*   **View article summaries:** Automatically generate a concise, three-sentence summary of each article using OpenAI.
*   **Read full articles:** Access the original article via a link provided in the app.
*   **View Article Image:** Display image and information of the selected articles.

## Tools Used

*   **Streamlit:** A Python library for building interactive web applications.
*   **News API:** A service providing access to news articles from various sources.
*   **OpenAI API:** A service providing access to powerful language models for text summarization.
*   **LangChain:** A framework for developing applications powered by language models.
*   **Python:** The primary programming language.
*   **`python-dotenv`:**  For managing API keys securely.

**Key Libraries:**

*   `newsapi-python`
*   `langchain`
*   `openai`
*   `streamlit`
*   `python-dotenv`

## Setup

1.  **Clone the repository:**

    ```bash
    git clone [your_repository_url]
    cd [your_repository_directory]
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Make sure you create a `requirements.txt` file.  Example below.)

4.  **Set up API keys:**

    *   Create a `.env` file in the root directory of the project.
    *   Add your News API and OpenAI API keys to the `.env` file:

        ```
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        NEWS_API_KEY=YOUR_NEWS_API_KEY
        ```

    *   **Important:** Never commit your `.env` file to a public repository!  Add it to your `.gitignore` file.

5.  **Run the application:**

    ```bash
    streamlit run news_summarizer_api.py
    ```

## Usage

1.  Open the application in your web browser (usually at `http://localhost:8501`).
2.  Use the sidebar to:
    *   Select a news source from the dropdown menu.
    *   Choose a date range for the articles.
3.  Click the "Fetch & Summarize" button.
4.  The application will display a list of articles from the selected source and date range.
5.  Expand each article to view the original content snippet and its AI-generated summary.
6.  Click the "Full Article" link to read the complete article on the news source's website.

## Blog Post: The Power of AI-Driven News Summarization

In today's fast-paced world, staying informed can feel like an overwhelming task.  With countless news sources and a constant stream of information, it's challenging to keep up with the stories that matter most. That's where AI-driven news summarization comes in.

This Cloud-Based News Summarizer project demonstrates how we can leverage the power of Artificial Intelligence to streamline the news consumption process. By combining the News API with OpenAI's language models, we can quickly extract the core essence of news articles, saving valuable time and effort.

**Key Benefits:**

*   **Efficiency:** Get the gist of a news article in seconds.
*   **Personalization:** Focus on news from sources you trust.
*   **Accessibility:** Make news more accessible to those with limited time or attention spans.

**The Future of News Consumption:**

AI-driven summarization is poised to revolutionize how we consume news.  Imagine a world where you can effortlessly stay informed about the topics that matter most to you, without being bogged down by lengthy articles.  This project is a small step towards that future.

## Contributing

We welcome contributions to this project!  Here are some ways you can contribute:

*   **Report bugs:**  If you find a bug, please create a new issue on GitHub.
*   **Suggest enhancements:**  Have an idea for a new feature?  Open an issue to discuss it.
*   **Submit pull requests:**  If you're comfortable with Git, you can submit a pull request with your changes.

**Contribution Guidelines:**

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes and commit them with clear and concise commit messages.
4.  Submit a pull request.
