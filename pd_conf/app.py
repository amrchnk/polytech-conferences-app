from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse, abort
import psycopg2
from datetime import datetime

app = Flask(__name__)

def db_get_conn():
    return psycopg2.connect(user = "postgres", password = "admin", host = "127.0.0.1", port = "5432", database = "PD_conference")

####################          CONFERENCES          ####################
@app.route("/new_conference", methods = ["POST"])
def create_conf():
    if not request.json:
        abort(400)

    d = request.json

    d["storage_id"] = create_storage()

    insert_req = """INSERT INTO conference (theme, date, organizer, link, storage_id, partner_list_id) VALUES ('{theme}', '{date}', '{organizer}', '{link}', {storage_id}, {partner_list_id})""".format(
        theme = d["theme"], date = datetime.strptime(d["date"], "%d/%m/%Y %H:%M"), organizer = d["organizer"], link = d["link"], storage_id = d["storage_id"], partner_list_id = d["partner_list_id"])

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(insert_req)
        connection.commit()
        print("Успешно добавлено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/conferences", methods = ["GET"])
def get_conferences():
    conferences = []

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT id, theme, date::timestamp, organizer, link, storage_id, partner_list_id FROM conference"""
        cursor.execute(select_req)
        data = cursor.fetchall()

        if len(data) > 0:
            for row in data:
                conferences.append(
                    {'id': row[0],
                    'theme': row[1],
                    'date': row[2],
                    'organizer': row[3],
                    'link': row[4],
                    'storage_id': row[5],
                    'partner_list_id': row[6]})
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(conferences)

@app.route("/conferences/<int:conference_id>", methods = ["PUT"])
def update_conference(conference_id):
    if not request.json:
        abort(400)

    d = request.json

    update_req = """UPDATE conference SET theme = '{theme}', date = '{date}', organizer = '{organizer}', link = '{link}' WHERE id = {conference_id}""".format(
        theme = d["theme"], date = datetime.strptime(d["date"], "%d/%m/%Y %H:%M"), organizer = d["organizer"], link = d["link"], conference_id = conference_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(update_req)
        connection.commit()
        print("Успешно изменено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/conferences/<int:conference_id>", methods = ["DELETE"])
def delete_conference(conference_id):
    delete_req = """DELETE FROM conference WHERE id = {}""".format(conference_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(delete_req)
        connection.commit()
        print("Успешно удалено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/conferences/<int:conference_id>", methods = ["GET"])
def get_conf_by_id(conference_id):
    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT theme, date::timestamp, organizer, link, storage_id, partner_list_id FROM conference WHERE id = {}""".format(conference_id)
        cursor.execute(select_req)
        data = cursor.fetchall()[0]            
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(
                theme = data[0],
                date = data[1],
                organizer = data[2],
                link = data[3],
                storage_id = data[4],
                partner_list_id = data[5])


####################          STORAGES          ####################
def create_storage():
    new_id = 0

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT MAX(id) FROM storage"""
        cursor.execute(select_req)
        max_id = cursor.fetchall()[0][0]

        if max_id is None:
            max_id = 0

        new_id = max_id + 1

        insert_req = """INSERT INTO storage (id) VALUES ({})""".format(new_id)

        cursor.execute(insert_req)
        connection.commit()
        print("Успешно добавлено")
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return new_id

@app.route("/conferences/<int:conference_id>/storage", methods = ["GET"])
def get_storage(conference_id):
    materials = []

    try:
        storage_id = get_storage_by_id(conference_id)
        if storage_id == 0:
            return "error"

        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT file.file_name FROM file JOIN storage_has_files ON file.id = storage_has_files.file_id AND storage_has_files.storage_id = {}""".format(storage_id)
        cursor.execute(select_req)
        data = cursor.fetchall()
        
        if len(data) > 0:
            for row in data:
                materials.append({'file_name': row[0]})
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(materials)

#@app.route("/conferences/<int:conference_id>/storage", methods = ["DELETE"])
def delete_storage(conference_id):
    try:
        storage_id = get_storage_by_id(conference_id)
        delete_req = """DELETE FROM storage WHERE id = {}""".format(storage_id)

        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(delete_req)
        connection.commit()
        print("Успешно удалено")
        answer = "success"
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

def get_storage_by_id(conference_id):
    storage_id = 0

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT storage_id FROM conference WHERE id = {}""".format(conference_id)
        cursor.execute(select_req)
        storage_id = cursor.fetchall()[0][0]
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return storage_id

####################          PARTNERS_LISTS          ####################
@app.route("/new_partners_list", methods = ["POST"])
def create_partners_list():
    if not request.json:
        abort(400)

    d = request.json
    new_id = 0

    select_req = """SELECT MAX(id) FROM partners_list"""

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(select_req)
        new_id = cursor.fetchall()[0][0] + 1

        insert_req = """INSERT INTO partners_list (id) VALUES ({})""".format(new_id)
        cursor.execute(insert_req)
        connection.commit()

        cursor.execute(select_req)
        new_id = cursor.fetchall()[0][0]
        print("Успешно добавлено")
        answer = jsonify(id = new_id)

        for row in d:
            answer_add = add_partner_in_list(new_id, row["partner_id"])
            if answer_add == "error":
                answer = "error"
                break
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners_lists/<int:partners_list_id>", methods = ["DELETE"])
def delete_partners_list(partners_list_id):
    delete_req = """DELETE FROM partners_list WHERE id = {}""".format(partners_list_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(delete_req)
        connection.commit()
        print("Успешно удалено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners_lists/<int:partners_list_id>/<int:partner_id>", methods = ["POST"])
def add_partner_in_list(partners_list_id, partner_id):
    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        insert_req = """INSERT INTO partners_list_has_partners (list_id, partner_id) VALUES ({list_id}, {partner_id})""".format(list_id = partners_list_id, partner_id = partner_id)
        cursor.execute(insert_req)
        connection.commit()
        print("Успешно добавлено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners_lists/<int:partners_list_id>/<int:partner_id>", methods = ["DELETE"])
def delete_partner_from_list(partners_list_id, partner_id):
    delete_req = """DELETE FROM partners_list_has_partners WHERE list_id = {list_id} AND partner_id = {partner_id}""".format(list_id = partners_list_id, partner_id = partner_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(delete_req)
        connection.commit()
        print("Успешно удалено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners_lists/<int:partners_list_id>", methods = ["GET"])
def get_partners_list_by_id(partners_list_id):
    partners = []

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT partner_id FROM partners_list_has_partners WHERE list_id = {}""".format(partners_list_id)
        cursor.execute(select_req)
        data = cursor.fetchall()
        
        if len(data) > 0:
            for row in data:
                partner= get_partner_by_id(row[0]).json
                partners.append(partner)
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(partners)

####################          PARTNERS          ####################
@app.route("/new_partner", methods = ["POST"])
def create_partner():
    if not request.json:
        abort(400)

    d = request.json

    insert_req = """INSERT INTO partners (id, partner, comment) VALUES (DEFAULT, '{partner}', '{comment}')""".format(partner = d["partner"], comment = d["comment"])

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(insert_req)
        connection.commit()
        print("Успешно добавлено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners/<int:partner_id>", methods = ["PUT"])
def update_partner(partner_id):
    if not request.json:
        abort(400)

    d = request.json

    update_req = """UPDATE partners SET partner = '{partner}', comment = '{comment}' WHERE id = {partner_id}""".format(
        partner = d["partner"], comment = d["comment"], partner_id = partner_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(update_req)
        connection.commit()
        print("Успешно изменено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = error
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners/<int:partner_id>", methods = ["DELETE"])
def delete_partner(partner_id):
    delete_req = """DELETE FROM partners WHERE id = {}""".format(partner_id)

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        cursor.execute(delete_req)
        connection.commit()
        print("Успешно удалено")
        answer = "success"
    except (Exception) as error:
        print("Ошибка при работе с базой данных", error)
        answer = "error"
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return answer

@app.route("/partners", methods = ["GET"])
def get_partners():
    partners = []

    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT * FROM partners"""
        cursor.execute(select_req)
        data = cursor.fetchall()

        if len(data) > 0:
            for row in data:
                partners.append(
                    {'id': row[0],
                    'partner': row[1],
                    'comment': row[2]})
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(partners)

@app.route("/partners/<int:partner_id>", methods = ["GET"])
def get_partner_by_id(partner_id):
    try:
        connection = db_get_conn()
        cursor = connection.cursor()
        select_req = """SELECT partner, comment FROM partners WHERE id = {}""".format(partner_id)
        cursor.execute(select_req)
        data = cursor.fetchall()[0]            
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(
                partner = data[0],
                comment = data[1])

####################          CONFERENCE_MEMBERS          ####################
@app.route("/conferences/<int:conference_id>/conf_members", methods = ["GET"])
def get_conf_members(conference_id):
    members = []

    try:
        connection = db_get_conn()
        cursor = connection.cursor()

        select_req = """SELECT full_name, conference_topic FROM users JOIN conference_member ON users.id = conference_member.user_id AND conference_member.conference_id = {}""".format(conference_id)
        cursor.execute(select_req)
        data = cursor.fetchall()

        if len(data) > 0:
            for row in data:
                members.append({'full_name': row[0],
                                'topic': row[1]})
    except(Exception) as error:
        print("Ошибка при работе с базой данных", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение закрыто")
            return jsonify(members)

#######################
# Добавление заголовка для корректной работы CORS
#@app.after_request
#def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    #response.headers.add('Access-Control-Allow-Origin', 'http://tpis-site.std-913.ist.mospolytech.ru')
    #response.headers.add('Access-Control-Allow-Headers', '*')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    #return response

if __name__ == '__main__':
    app.run()