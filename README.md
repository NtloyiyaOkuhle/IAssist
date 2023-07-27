# IAssist
Intelligent Personal Assistant with Voice and Text Interaction

Description:
This Python script showcases an intelligent personal assistant that can interact with users through both voice and text inputs. The assistant utilizes several powerful libraries to provide a seamless user experience.

Features:

    Web Scraping: The assistant can perform web scraping on popular search engines such as Google, Bing, Yahoo, and DuckDuckGo to retrieve information based on user queries.

    Text-to-Speech: It utilizes the Pyttsx3 library to convert text responses into speech, enabling voice-based interaction with users.

    Speech Recognition: The assistant integrates the SpeechRecognition library to convert voice inputs from users into text, facilitating effortless voice interaction.

    Natural Language Processing (NLP): Basic keyword matching is employed as a simple NLP technique to determine the user's intent. It recognizes user queries related to weather and news, enabling context-aware responses.

How It Works:
The Flask web framework is utilized to create a user-friendly interface where users can enter their queries through a text box. Additionally, users can choose to interact with the assistant using voice input. When voice input is selected, the SpeechRecognition library captures the user's voice and converts it into text. The assistant then processes the query using the NLP technique to recognize the intent.

For weather-related queries, the assistant responds with the current weather status, while for news-related queries, it provides the latest news headlines. For general queries, the assistant performs a web search on Google.

The assistant's responses are presented both as speech (for voice interaction) and as text (for text-based interaction) on the web application.

Note: To ensure proper functionality, the script uses appropriate User-Agent headers to mimic browser requests when performing web scraping.

Experience the convenience of this Intelligent Personal Assistant by running the code and interacting with it using either voice or text inputs!
