import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Function to perform web scraping and get results from Google
def search_google(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
        if results:
            return results[0].get_text()
    except requests.exceptions.RequestException as e:
        return f"Error occurred while searching Google: {e}"
    return None

# Function to perform web scraping and get results from Bing
def search_bing(query):
    try:
        url = f"https://www.bing.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="b_algo")
        if results:
            return results[0].get_text()
    except requests.exceptions.RequestException as e:
        return f"Error occurred while searching Bing: {e}"
    return None

# Function to perform web scraping and get results from Yahoo
def search_yahoo(query):
    try:
        url = f"https://search.yahoo.com/search?p={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="dd algo")
        if results:
            return results[0].get_text()
    except requests.exceptions.RequestException as e:
        return f"Error occurred while searching Yahoo: {e}"
    return None

# Function to perform web scraping and get results from DuckDuckGo
def search_duckduckgo(query):
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__url")
        if results:
            return results[0].get_text()
    except requests.exceptions.RequestException as e:
        return f"Error occurred while searching DuckDuckGo: {e}"
    return None

# Function to initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    # Adjust the rate and voice properties
    engine.setProperty("rate", 150)  # You can adjust the speed (words per minute) here
    engine.setProperty("voice", "english+f4")  # Use a more human-like voice, if available
    engine.say(text)
    engine.runAndWait()

# Function to process user query and return the answer from the appropriate search engine
def get_answer(query):
    search_engines = ["Google", "Bing", "Yahoo", "DuckDuckGo"]
    for engine in search_engines:
        result = None
        if engine == "Google":
            result = search_google(query)
        elif engine == "Bing":
            result = search_bing(query)
        elif engine == "Yahoo":
            result = search_yahoo(query)
        elif engine == "DuckDuckGo":
            result = search_duckduckgo(query)
        
        if result:
            return engine, result
    
    return None, "No results found for your query."
# Function to process user query using NLP and return intent
def process_query_nlp(query):
    # Use basic keyword matching as a simple NLP technique
    if "weather" in query:
        return "WeatherIntent"
    elif "news" in query:
        return "NewsIntent"
    else:
        return "GeneralIntent"
# Function to respond to user query based on the recognized intent
def respond_to_intent(intent, query):
    if intent == "WeatherIntent":
        # Perform action for weather query (e.g., use a weather API)
        response = "The weather today is sunny."
    elif intent == "NewsIntent":
        # Perform action for news query (e.g., use a news API)
        response = "Here are the latest news headlines."
    else:
        # For general queries, perform a Google search
        response = search_google(query)

    return response

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["query"]

        # Check if the query is text or voice input
        is_voice_input = request.form.get("voice_input")

        if is_voice_input:
            # If voice input, use SpeechRecognition to convert it to text
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                query = recognizer.recognize_google(audio)
                print("You said:", query)
            except sr.UnknownValueError:
                query = ""
                print("Could not understand audio.")
            except sr.RequestError as e:
                query = ""
                print(f"Error occurred while processing audio: {e}")

        intent = process_query_nlp(query)
        response = respond_to_intent(intent, query)  # Pass the 'query' variable as an argument

        if is_voice_input:
            speak(response)  # Speak the response for voice-based interaction
        else:
            # Render the response in the web application for text-based interaction
            return render_template("index.html", answer=response, source="")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
