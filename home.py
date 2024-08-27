from flask import Flask, render_template, render_template_string, url_for, request,redirect

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get("Librarian-submit"):
            return redirect(url_for('Librarian'))
        if request.form.get("Student-submit"):
            return redirect(url_for('Student'))

    else:
        return render_template("index.html")


@app.route('/Librarian', methods = ['POST', 'GET'])
def Librarian():
    return render_template('librarian.html')

@app.route('/Student', methods = ['POST', 'GET'])
def Student():
    return render_template('student.html')

if __name__ == '__main__':
    app.run(debug=True)