from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    print("请求到了哈哈哈")
    return "hello world!"

if __name__ == '__main__':
    app.run(debug=True)

