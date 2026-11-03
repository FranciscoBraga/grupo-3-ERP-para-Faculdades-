function mostra(t) {
  document.getElementById("prof").style.display = "none"
  document.getElementById("ponto").style.display = "none"
  document.getElementById("alunos").style.display = "none"
  document.getElementById("matricula").style.display = "none"
  document.getElementById(t).style.display = "block"
}

function salvarProfessor() {
  var dados = {
    nome: document.getElementById("pnome").value,
    cpf: document.getElementById("pcpf").value,
    email: document.getElementById("pemail").value,
    senha: document.getElementById("psenha").value,
    salario: document.getElementById("psalario").value
  }
  fetch("/professores", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(dados)})
  listarProfessores()
}

function listarProfessores() {
  fetch("/professores").then(r => r.json()).then(l => {
    var h = ""
    for (var i = 0; i < l.length; i++) {
      h += l[i][1] + " - " + l[i][2] + " - " + l[i][4] + " - R$" + l[i][5] + "<br>"
    }
    document.getElementById("listaProf").innerHTML = h
  })
}

function baterPonto(tipo) {
  var id = document.getElementById("pontoId").value
  fetch("/ponto/" + tipo, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({professor_id: id})})
    .then(r => r.json()).then(d => alert(d.msg))
}

function relatorio() {
  var id = document.getElementById("pontoid").value
  fetch("/ponto/relatorio/" + id).then(r => r.json()).then(d => {
    document.getElementById("relPonto").innerText = JSON.stringify(d)
  })
}

function salvarAluno() {
  var dados = {
    nome: document.getElementById("anome").value,
    cpf: document.getElementById("acpf").value,
    curso: document.getElementById("acurso").value
  }
  fetch("/alunos", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(dados)})
    .then(r => r.json()).then(d => alert("RA: " + d.ra))
  listarAlunos()
}

function listarAlunos() {
  fetch("/alunos").then(r => r.json()).then(l => {
    var h = ""
    for (var i = 0; i < l.length; i++) {
      h += l[i][1] + " - " + l[i][2] + " - " + l[i][3] + " - " + l[i][4] + "<br>"
    }
    document.getElementById("listaAlunos").innerHTML = h
  })
}

function matricular() {
  var dados = {
    aluno_id: document.getElementById("maluno").value,
    disciplina_id: document.getElementById("mdisc").value,
    semestre: document.getElementById("msem").value,
    bolsista: document.getElementById("mbolsa").value
  }
  fetch("/matricula", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(dados)})
    .then(r => r.json()).then(d => {
      document.getElementById("resMat").innerHTML = d.msg + " valor: " + d.valor
    })
}

mostra("prof")
listarProfessores()
