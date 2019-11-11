from flask import Flask, render_template,request,jsonify
from Db.Database import Database
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    print("请求到了哈哈哈")
    return "hello world!"

@app.route("/test",methods=['POST'])
def test():
	return "testalsdjflasjdflasjkdfljkasd"

@app.route("/init_data")
def init_data():
    title_list = Database().select()
    return jsonify(title_list)

@app.route("/add_article")
def add_article():
	article_name = request.args.get('article_name')
	Id = Database().add(article_name,"")
	return jsonify({'Id':Id})

# 获取文章内容
@app.route("/get_article")
def get_article():
	Id = request.args.get("Id")
	content = Database().get(int(Id))
	return jsonify({"content":content})

# 保存文章内容
@app.route("/save_content",methods=['POST'])
def save_content():
	result = request.get_json()["result"]
	Id = result['Id']
	content = result['content']
	# print(result)
	Database().editContent(Id,content)
	return jsonify({"status":200})

@app.route("/delete_article")
def delete_article():
	Id = request.args.get("Id")
	Database().deleteArticle(int(Id))
	return jsonify({"status":200})

if __name__ == '__main__':
    app.run(debug=True)

