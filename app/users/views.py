from . import user_bp
from flask import request, redirect, url_for, render_template, session, flash, make_response
from datetime import timedelta, datetime

users = {
    "user1": "user1",
    "testUser": "testUser",
    "guest1": "guest1",
    "111": "111",
    "User": "Password"
}
@user_bp.route('/')
def main():
    return render_template("base.html")

@user_bp.route('/resume')
def show_resume():
    return render_template("resume.html")

@user_bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)




@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

@user_bp.route('/set_color/<color>')
def set_color(color):
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('color_scheme', color)
    return response


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("login")
        password = request.form.get("password")
        
        # Перевірка автентифікації
        if users.get(username) == password:
            session['username'] = username
            flash("Success: You have logged in successfully.", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Error: Invalid username or password.", "danger")
    
    return render_template("login.html")
@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if "username" in session:
        if request.method == 'POST':
            response = make_response(redirect(url_for('users.profile')))

            # Додавання кукі
            if 'key-cookie' in request.form and 'value-cookie' in request.form and 'expires' in request.form:
                key = request.form['key-cookie']
                value = request.form['value-cookie']
                try:
                    expires = int(request.form['expires'])
                    response.set_cookie(key, value, max_age=expires)
                    flash(f'Кука "{key}" успішно додана!', 'success')
                except ValueError:
                    flash('Помилка: Термін дії має бути числом.', 'danger')
                return response

            # Видалення кукі за ключем
            if 'delete-cookie' in request.form:
                key = request.form['delete-cookie']
                if key in request.cookies:
                    response.set_cookie(key, '', expires=0)
                    flash(f'Кука "{key}" успішно видалена!', 'success')
                else:
                    flash(f'Кука "{key}" не знайдена.', 'danger')
                return response

            # Видалення всіх кукі
            if 'delete-all-cookies' in request.form:
                for cookie in request.cookies:
                    response.set_cookie(cookie, '', expires=0)
                flash('Усі кукі успішно видалені!', 'success')
                return response

        username_value = session["username"]
        cookies = request.cookies
        return render_template("profile.html", username=username_value, cookies=cookies)

    flash("Невірна сесія. Увійдіть, будь ласка.", "danger")
    return redirect(url_for("users.login"))




@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('users.login'))

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60), path='/')
    # Якщо ви хочете просто видалити куку color, ви можете зробити це
    response.set_cookie('color', '', expires=0, path='/')  # видаляємо куку color
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Користувач: {username}'
    return 'Кука не знайдена'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0, path='/')  # видаляємо куку username
    return response