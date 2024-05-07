# import blueprint
from app.auth import bp
# flask modules
from flask import render_template, request, session, redirect
from app.extensions import db
from app.models.profile import Profile


def redirect_with_message(message, href):
    return f"<script>alert('{message}'); location.href = '{href}'</script>"


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'login' in session:
            return redirect('/')
        return render_template("login.html")
    else:
        login = request.form.get("login", None)
        password = request.form.get("password", None)
        if not login or not password:
            return redirect_with_message("Все поля должны быть заполнены!", "/login")
        profiles = db.session.query(Profile).filter((Profile.login == login)|(Profile.password == password)).all()
        if len(profiles):
            session['login'] = login
            session['password'] = password
            return redirect_with_message("Вход успешно выполнен", "/login")
        else:
            return redirect_with_message("Неправильные данные или данной учетней записи не существует", "/login")


@bp.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        if 'login' in session:
            return redirect('/')
        return render_template("registration.html")
    else:
        fullname = request.form.get("fullname", "н/з") or "н/з"
        login = request.form.get("login", None)
        password = request.form.get("password", None)
        phone = request.form.get("phone", None)
        email = request.form.get("email", "н/з")
        if not login or not password or not phone:
            return redirect_with_message("Одно из важных полей не заполнено", "/registration")
        profiles = db.session.query(Profile).filter((Profile.login == login)).all()
        if len(profiles)>0:
            return redirect_with_message("Учетная запись с веденными данными уже существует", "/registration")
        profile = Profile(fullname=fullname, login=login, password=password, phone_num=phone, email=email)
        db.session.add(profile)
        db.session.commit()
        return redirect_with_message("Учетная запись успешно создана", "/login")
