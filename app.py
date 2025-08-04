from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from src.rag import graph

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Time Travel LLM - 1861</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }
            textarea {
                width: 100%;
                height: 100px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                resize: vertical;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
            }
            button:hover {
                background-color: #0056b3;
            }
            button:disabled {
                background-color: #ccc;
                cursor: not-allowed;
            }
            .response {
                margin-top: 30px;
                padding: 20px;
                background-color: #f8f9fa;
                border-left: 4px solid #007bff;
                border-radius: 5px;
                white-space: pre-wrap;
                font-size: 16px;
                line-height: 1.6;
            }
            .loading {
                text-align: center;
                color: #666;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕰️ Time Travel LLM - 1861</h1>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">
                Ask questions and get answers as if you're talking to someone from 1861
            </p>
            
            <form id="questionForm">
                <div class="form-group">
                    <label for="question">What would you like to ask someone from 1861?</label>
                    <textarea id="question" name="question" placeholder="e.g., How can I treat a fever? What's happening with the war? What's the latest news from Washington?" required></textarea>
                </div>
                <button type="submit" id="submitBtn">Ask Question</button>
            </form>
            
            <div id="response" style="display: none;"></div>
        </div>

        <script>
            document.getElementById('questionForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const question = document.getElementById('question').value;
                const submitBtn = document.getElementById('submitBtn');
                const responseDiv = document.getElementById('response');
                
                // Show loading state
                submitBtn.disabled = true;
                submitBtn.textContent = 'Thinking...';
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = '<div class="loading">Searching through 1861 newspapers and thinking like someone from that time...</div>';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: question })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        responseDiv.innerHTML = '<div class="response">' + data.response + '</div>';
                    } else {
                        responseDiv.innerHTML = '<div class="response" style="border-left-color: #dc3545; color: #dc3545;">Error: ' + data.error + '</div>';
                    }
                } catch (error) {
                    responseDiv.innerHTML = '<div class="response" style="border-left-color: #dc3545; color: #dc3545;">Error: Could not connect to the server. Please try again.</div>';
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Ask Question';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'Please provide a question'})
        
        # Use your existing RAG graph
        result = graph.invoke({"question": question})
        response = result["response"]
        
        return jsonify({'success': True, 'response': response})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting Time Travel LLM - 1861")
    print("📖 Make sure you have your OpenAI API key in a .env file")
    print("🌐 Open your browser to: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8000) 