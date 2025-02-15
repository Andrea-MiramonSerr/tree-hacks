from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)

# Define the home route with a form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return render_template('result.html', name=name, message=message)
    return render_template('index.html')

# Additional route example
@app.route('/about')
def about():
    return render_template('about.html')

# The main function to run the app
if __name__ == '__main__':
    app.run(debug=True)