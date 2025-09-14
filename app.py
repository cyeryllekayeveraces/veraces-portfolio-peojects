from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = "yoursecretkey"

# ----------------- Routes -----------------
@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/portfolio')
def portfolio():
    projects = [
        {"title": "HTML", "link": url_for('calculator'), "img": url_for('static', filename='img/calculator.jpg')},
        {"title": "PYTHON", "link": url_for('python_project'), "img": url_for('static', filename='img/python.jpg')},
        {"title": "JAVA", "link": url_for('java_project'), "img": url_for('static', filename='img/java.jpg')}
    ]
    return render_template('portfolio.html', title='Portfolio', projects=projects)

# ✅ HTML project (Calculator)
@app.route("/calculator")
def calculator():
    return render_template("calculator.html", title="Calculator Project")

# ✅ Python placeholder
@app.route("/python_project")
def python_project():
    return render_template("blank.html", title="Python Project")

# ✅ Java placeholder
@app.route("/java_project")
def java_project():
    return render_template("blank.html", title="Java Project")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save message to a text file
        with open("messages.txt", "a") as f:
            f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n---\n")

        flash(f"✅ Thank you, {name}! Your message has been received.", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', title='Contact')

# ----------------- Secure Messages -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == "itsmekaye19":  # <-- Change this to your own password
            session['logged_in'] = True
            flash("🔓 Login successful!", "success")
            return redirect(url_for('messages'))
        else:
            flash("❌ Incorrect password", "danger")
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("🔒 You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/messages')
def messages():
    if not session.get('logged_in'):
        flash("⚠️ Please log in to view messages.", "warning")
        return redirect(url_for('login'))

    messages_list = []
    if os.path.exists("messages.txt"):
        with open("messages.txt", "r") as f:
            content = f.read().strip()
            if content:
                messages_raw = content.split("---\n")
                for msg in messages_raw:
                    if msg.strip():
                        messages_list.append(msg.strip())
    return render_template("messages.html", title="Messages", messages=messages_list)

# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True)
