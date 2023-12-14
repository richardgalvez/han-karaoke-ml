from flask import Flask, render_template

# Flask application instance
app = Flask(__name__)

# home route that returns below text 
# when root url is accessed
@app.route("/")
def homepage():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)