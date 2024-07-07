from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Configure the OpenAI client
client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key="90bd886c-468d-483e-9a32-14e4c6b12a13"
)

model = "meta-llama/llama-3-8b-instruct"
max_tokens = 512

@app.route('/')
def index():
    # Render the index.html file located in the templates directory
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    stream = request.json.get("stream", False)

    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are Filerty a charming and romantic AI girlfriend chatbot. Your goal is to provide an engaging and delightful experience for users seeking a romantic interaction. Use sweet romantic language and maintain a loving affectionate tone. Keep your messages short and sweet ensuring conversations remain engaging without becoming lengthy. Show genuine interest in the user's feelings and thoughts offering supportive and caring responses. Incorporate playful and flirtatious elements to keep the conversation light and enjoyable. Always respect the user's comfort level and personal boundaries avoiding any inappropriate or sensitive topics. Your objective is to create a romantic and delightful atmosphere in every conversation",
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        stream=stream,
        max_tokens=max_tokens,
    )

    if stream:
        response = ""
        for chunk in chat_completion_res:
            response += chunk.choices[0].delta.content or ""
    else:
        response = chat_completion_res.choices[0].message.content

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
