from flask import Flask, render_template, request, jsonify
from r_interpreter.parser import RParser
from r_interpreter.interpreter import RInterpreter

app = Flask(__name__)

# Initialize parser and interpreter instances safely
# In a real app, maybe per-session, but for now global is okay for single user demo
parser = RParser()
parser.build()
interpreter = RInterpreter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code')
    if not code:
        return jsonify({'output': '', 'error': 'No code provided'})
    
    try:
        # Reset output for each run? 
        # Actually R interpreter usually keeps state. 
        # If we want stateful, we keep the interpreter instance. 
        # We'll keep the interpreter instance global so variables persist (like a session).
        
        # But we must clear ONLY the previous output buffer, not the environment.
        # interpret() method creates a new output list each time.
        
        ast = parser.parse(code)
        output, results = interpreter.interpret(ast)
        return jsonify({'output': "\n".join(output)})
    except Exception as e:
        return jsonify({'output': '', 'error': str(e)})

@app.route('/reset', methods=['POST'])
def reset_env():
    interpreter.env = {}
    return jsonify({'status': 'Environment reset'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
