from flask import Flask, render_template, render_template_string, url_for, request,redirect


# ----- CREATE Student / Librarian based on the FILE Called during INVOKE
def Register_user_function(User_email,User_name,FileName):
    with open(FileName, "r+") as user_tab:
        dataList = user_tab.readlines()
        unique_Name = []
        for i in dataList:
            entry = i.split(',')
            unique_Name.append(entry[0])
        if User_name not in unique_Name:
            user_tab.writelines(f'{User_name},{User_email}\n')
        elif User_name in unique_Name:
            return redirect(url_for("Student_landingpage",User_Name = User_name))
    return True

# ----- VERIFY if a Student / Librarian based on the FILE called during INVOKE
def verify_user(User_email,User_name,FileName):
    with open(FileName,"r") as user_tab:
        dataList = user_tab.readlines()
        check_string = User_name + "," + User_email + "\n"
        if check_string in dataList:
            return True
        else:
            return redirect(url_for("Register_Yourself_post_login"))

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


@app.route('/Librarian/<User_Name>', methods = ['POST', 'GET'])
def Librarian_Landingpage(User_Name):
    if request.method == 'POST':
        if request.form.get("Check Book Status"):
            return redirect(url_for("Books_Directory"))
        if request.form.get("Enter New Books"):
            return redirect(url_for("Return_Books"))
        if request.form.get("Check Book Transactions"):
            return redirect(url_for("Book_Transactions"))
    else:
        return render_template('librarian.html')
    

# ----- BOOK TABLE -----

@app.route('/Books',methods = ['POST','GET'])
def search_books():
    return render_template("Book/Book-View.html")


# ----- EVERYTHING RELATED TO STUDENTS -----

# ----- STUDENT LOGIN / REGISTER -----
@app.route('/Student',methods = ['POST','GET'])
def Student():
    if request.method == 'POST':
        if request.form.get("Register-New-Student"):
            return redirect(url_for("student_register"))
        if request.form.get("Login-Existing-Student"):
            return redirect(url_for("student_Login"))
    return render_template("student.html")


# ----- STUDENT REGISTRATION PAGE -----
@app.route('/Student/Register',methods = ['POST','GET'])
def student_register():
    if request.method == 'POST':
        student_name = request.form['Student-Name']
        student_email = request.form['Student-Email']
        # Call function to write down if the user doesn't exist
        if Register_user_function(student_email,student_name,"Student_details.csv") == True:
            return redirect(url_for("student_success_register",stud_email = student_email, stud_name = student_name))
        else:
            return redirect(url_for("Error"))
    else:    
        return render_template("Student/Student-Register.html")
    
# ----- STUDENT REGISTER SUCCESS -----    
@app.route('/Student/Register/Success', methods = ['POST','GET'])
def student_success_register():
    stud_name = request.args.get('stud_name',None)
    stud_email = request.args.get('stud_email',None)
    return render_template("Student/Student-Register-Success.html",student_email = stud_email,student_name = stud_name)

# ----- STUDENT LOGIN PAGE -----
@app.route('/Student/Login', methods = ['POST', 'GET'])
def student_Login():
    if request.method == 'POST':
        stud_name = request.form['Student-Name']
        stud_email = request.form['Student-Email']
        if verify_user(stud_email,stud_name,"Student_details.csv") == True:
            print("User verified, existing in DB.")
            return redirect(url_for("Student_landingpage",User_Name = stud_name))
    return render_template("Student/student-Login.html")

# ----- STUDENT LANDING PAGE -----
@app.route('/Student/<User_Name>', methods = ['POST', 'GET'])
def Student_landingpage(User_Name):
    if request.method == 'POST':
        if request.form.get("Search-Books"):
            return redirect(url_for("search_books"))
        if request.form.get("Return-Book"):
            return redirect(url_for("return_book"))
    return render_template('Student/student-Landing.html',UserName = User_Name)

if __name__ == '__main__':
    app.run(debug=True)