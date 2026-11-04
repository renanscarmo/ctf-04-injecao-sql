# CTF 04: Injeção de SQL

Projeto criado a partir do [template-seguranca](https://github.com/renanscarmo/template-seguranca)
para praticar segurança em Python.

## Objetivo

Entrar na área restrita sem saber a senha, usando injeção de SQL, e depois corrigir a falha.

## Como foi

1. **Antes:** a consulta SQL era montada juntando texto com o que o usuário digitava. Com `admin' --` no campo de usuário, a verificação da senha era ignorada.
2. **Detecção:** o Bandit acusou a falha (B608, CWE-89) e o pipeline ficou vermelho.
3. **Depois:** a consulta usa parâmetros (`?`) e a senha é conferida por hash. Os mesmos ataques passaram a falhar e o pipeline voltou a ficar verde.

## O que aprendi

- Texto digitado pelo usuário nunca deve ser colado dentro de um comando SQL
- Na injeção de SQL, o `'` fecha o texto e o `--` comenta o resto da consulta
- Consultas parametrizadas separam o comando dos dados, e o que o usuário digita é sempre tratado como dado
- O Bandit reconhece esse padrão (B608), mas só com confiança baixa: o teste manual confirma
- A senha é conferida por hash, e não comparada dentro do SQL

## Ferramentas

- SAST com Bandit
- SCA com pip-audit
- GitHub Actions
