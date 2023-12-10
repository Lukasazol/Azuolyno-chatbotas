from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'

# Initialize the conversation history with a default message
conversation = [
    {"role": "assistant", "content": "Welcome! Let's chat."},
    {"role": "user", "content": "Vytautas Narmontas, Lina Daujotė ir Daiva Railienė yra Ąžuolyno gimnazijos mokytojai, kurie atitinkamai moko vaikus matematikos, lietuvių kalbos ir robotikos, x, y ir z kabinetuos. Naudok šią informaciją toliamesniame pokalbyje su manimi"}
]

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    global conversation  # Use global variable for conversation history

    # Get the user's message from the POST request
    user_message = request.json.get("message")

    # Append the user's message to the conversation history
    conversation.append({"role": "user", "content": user_message})

    # Send the conversation history to OpenAI's API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Extract and append the chatbot's response to the conversation history
    bot_message = response.choices[0].message["content"]
    conversation.append({"role": "assistant", "content": bot_message})

    # Return the chatbot's response
    return jsonify({"content": bot_message})

if __name__ == '__main__':
    app.run()
