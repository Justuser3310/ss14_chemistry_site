from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main():
	return render_template("index.html")

if __name__ == '__main__':
  app.run(debug=False, port = 5001)

@app.route("/submit", methods=['POST'])
def calculate():
  selectedval = request.form["getrecept"]
  return f"{selectedval}"