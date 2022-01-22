import smtplib

from flask import Flask, jsonify, request, abort
import psycopg2
app = Flask(__name__)
application = app
wsgi_app = app.wsgi_app
db_params = "dbname=PD_conference user=postgres password=zmp24DS"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login/<string:user>/<string:password>')
def login(user, password):
    conn = psycopg2.connect(db_params)
    cursor = conn.cursor()
    cursor.execute("select u.id as user_id, u.full_name as full_name, "
                   "r.id as role_id, role as role_name, comment as role_comment "
                   "from users u left join users_have_roles uhr "
                   "on u.id = uhr.user_id join roles r on r.id = uhr.role_id where u.login = %s and u.password = %s",
                   (user, password))
    data = cursor.fetchall()
    data_list = []
    if len(data) > 0:
        for item in data:
            data_list.append({
                'user_id': item[0],
                'full_name': item[1],
                'role_id': item[2],
                'role_name': item[3],
                'role_comment': item[4]
            })
    return jsonify(data_list)


@app.route('/reg', methods=['POST'])
def reg():
    # Если пришёл не JSON - возвращаем HTTP ошибку 400
    if not request.json:
        print(request.json)
        abort(400)
    d = request.json
    conn = psycopg2.connect(db_params)
    cursor = conn.cursor()
    # Ищем пользователя
    cursor.execute(
        "INSERT INTO users (`full_name`, `login`) values (%s, %s)",
        (d["full_name"], d["email"]))
    id_user = cursor.lastrowid
    conn.commit()

    conn = psycopg2.connect(db_params)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO storage (id) values (default)")
    id_storage = cursor.lastrowid
    conn.commit()
    for file_data in d["files"]:
        with open("files/" + file_data["file_name"], "wb") as file:
            file.write(file_data["file_data"])
            conn = psycopg2.connect(db_params)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO file (file_name) values (%s)", ("files/" + file_data["file_name"]))
            id_file = cursor.lastrowid
            conn.commit()
            conn = psycopg2.connect(db_params)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO storage_has_files (storage_id, file_id) values (%s, %s)", (id_storage, id_file))
            conn.commit()
    conn = psycopg2.connect(db_params)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conference_member (`conference_id`, `storage_id`, `user_id`, `conference_topic`) "
        "values (%s, %s, %s, %s)",
        (d["conference_id"], id_storage, id_user, d["conference_topic"]))
    HOST = "smtp.mail.ru"
    SUBJECT = "Conference registration"
    TO = d["email"]
    FROM = "ip_project_2021@mail.ru"
    text = "Conference registration completed. Your "
    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
    ))
    server = smtplib.SMTP(HOST, 25)
    server.starttls()
    server.login("ip_project_2021@mail.ru", "IPFiveSemester")
    server.sendmail(FROM, [TO], BODY)
    server.quit()
    return "1"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://ipsite.std-982.ist.mospolytech.ru')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



if __name__ == '__main__':
    app.run()
