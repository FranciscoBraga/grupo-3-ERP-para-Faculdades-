ERP FACULDADE
=============

Sistema completo para gestão da faculdade. Pronto para produção.

### Módulos
* Ponto eletrônico de professores (com biometria)
* Matrículas
* Financeiro / boletos
* Notas e frequência
* Portal do aluno

### Instalação

    pip install -r requirements.txt
    flask run --port 8080

Usuário: secretaria  
Senha: faculdade2020

### Banco de dados

Usar MySQL. Criar o banco `erp_fac` antes de rodar o script `banco.sql`.

### Regras de negócio

- Matrícula custa R$ 10,00 por hora-aula
- Bolsistas têm 30% de desconto
- Professor que não completar 180h/mês tem desconto no salário

### API

| rota | método |
|------|--------|
| /professor | POST |
| /aluno | GET |
| /matricula | POST |
