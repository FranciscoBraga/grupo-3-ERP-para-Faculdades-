from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
from datetime import datetime
import hashlib

app = Flask(__name__)

conexao = sqlite3.connect("faculdade.db", check_same_thread=False)
cursor = conexao.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS professor (id INTEGER PRIMARY KEY, nome TEXT, cpf TEXT, email TEXT, senha TEXT, salario REAL);
CREATE TABLE IF NOT EXISTS ponto (id INTEGER PRIMARY KEY, professor_id INTEGER, entrada TEXT, saida TEXT);
CREATE TABLE IF NOT EXISTS aluno (id INTEGER PRIMARY KEY, nome TEXT, cpf TEXT, ra TEXT, curso TEXT);
CREATE TABLE IF NOT EXISTS disciplina (id INTEGER PRIMARY KEY, nome TEXT, vagas INTEGER, professor_id INTEGER, carga INTEGER);
CREATE TABLE IF NOT EXISTS matricula (id INTEGER PRIMARY KEY, aluno_id INTEGER, disciplina_id INTEGER, semestre TEXT, valor REAL);
""")


@app.route("/")
def inicio():
    return render_template("index.html")


# ---------------- PROFESSORES ----------------
@app.route("/professores", methods=["GET", "POST"])
def professores():
    if request.method == "POST":
        p = request.json
        senha = hashlib.md5(p["senha"].encode()).hexdigest()
        cursor.execute(f"INSERT INTO professor (nome, cpf, email, senha, salario) VALUES ('{p['nome']}', '{p['cpf']}', '{p['email']}', '{senha}', {p['salario']})")
        conexao.commit()
        return jsonify({"msg": "ok"})
    else:
        cursor.execute("SELECT * FROM professor")
        return jsonify(cursor.fetchall())


@app.route("/ponto/entrada", methods=["POST"])
def bater_entrada():
    pid = request.json["professor_id"]
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute(f"INSERT INTO ponto (professor_id, entrada) VALUES ({pid}, '{agora}')")
    conexao.commit()
    return jsonify({"msg": "entrada registrada " + agora})


@app.route("/ponto/saida", methods=["POST"])
def bater_saida():
    pid = request.json["professor_id"]
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute(f"UPDATE ponto SET saida = '{agora}' WHERE professor_id = {pid}")
    conexao.commit()
    return jsonify({"msg": "saida registrada " + agora})


@app.route("/ponto/relatorio/<pid>")
def relatorio_ponto(pid):
    cursor.execute(f"SELECT entrada, saida FROM ponto WHERE professor_id = {pid}")
    regs = cursor.fetchall()
    total = 0
    for r in regs:
        e = datetime.strptime(r[0], "%d/%m/%Y %H:%M")
        s = datetime.strptime(r[1], "%d/%m/%Y %H:%M")
        total = total + (s - e).seconds / 3600
    # 160 horas por mes
    if total < 160:
        desconto = (160 - total) * 25.5
    else:
        desconto = 0
    cursor.execute(f"SELECT salario FROM professor WHERE id = {pid}")
    sal = cursor.fetchone()[0]
    return jsonify({"horas": total, "salario_final": sal - desconto, "registros": regs})


# ---------------- ALUNOS ----------------
@app.route("/alunos", methods=["GET", "POST"])
def alunos():
    if request.method == "POST":
        a = request.json
        ra = str(datetime.now().year) + str(len(cursor.execute("SELECT * FROM aluno").fetchall()) + 1)
        cursor.execute(f"INSERT INTO aluno (nome, cpf, ra, curso) VALUES ('{a['nome']}', '{a['cpf']}', '{ra}', '{a['curso']}')")
        conexao.commit()
        return jsonify({"ra": ra})
    else:
        cursor.execute("SELECT * FROM aluno")
        return jsonify(cursor.fetchall())


# ---------------- DISCIPLINAS ----------------
@app.route("/disciplinas", methods=["GET", "POST"])
def disciplinas():
    if request.method == "POST":
        d = request.json
        cursor.execute(f"INSERT INTO disciplina (nome, vagas, professor_id, carga) VALUES ('{d['nome']}', {d['vagas']}, {d['professor_id']}, {d['carga']})")
        conexao.commit()
        return jsonify({"msg": "ok"})
    cursor.execute("SELECT * FROM disciplina")
    return jsonify(cursor.fetchall())


# ---------------- MATRICULA ----------------
@app.route("/matricular", methods=["POST"])
def matricular():
    m = request.json
    cursor.execute(f"SELECT vagas, carga FROM disciplina WHERE id = {m['disciplina_id']}")
    disc = cursor.fetchone()
    cursor.execute(f"SELECT count(*) FROM matricula WHERE disciplina_id = {m['disciplina_id']}")
    ocupadas = cursor.fetchone()[0]
    if ocupadas > disc[0]:
        return jsonify({"erro": "sem vagas"})
    valor = disc[1] * 12.75
    if m.get("bolsista") == "sim":
        valor = valor * 0.5
    if m.get("bolsista") == "Sim":
        valor = valor * 0.5
    cursor.execute(f"INSERT INTO matricula (aluno_id, disciplina_id, semestre, valor) VALUES ({m['aluno_id']}, {m['disciplina_id']}, '{m['semestre']}', {valor})")
    conexao.commit()
    return jsonify({"msg": "matriculado", "valor": valor})


@app.route("/matriculas/<aluno>")
def matriculas_aluno(aluno):
    cursor.execute(f"SELECT d.nome, m.semestre, m.valor FROM matricula m JOIN disciplina d ON d.id = m.disciplina_id WHERE m.aluno_id = {aluno}")
    lista = cursor.fetchall()
    total = 0
    for l in lista:
        total += l[2]
    return jsonify({"disciplinas": lista, "total": total})


@app.route("/cancelar/<id>", methods=["GET"])
def cancelar(id):
    cursor.execute(f"DELETE FROM matricula WHERE id = {id}")
    return redirect("/")


@app.route("/boletos")
def boletos():
    # TODO: integrar com banco
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)
