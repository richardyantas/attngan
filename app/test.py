from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    

# 18.230.196.140:5000