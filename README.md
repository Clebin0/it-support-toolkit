<div align="center">

# IT Support Toolkit

**Diagnóstico · Infraestrutura · Evidências · Read-only**

<img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-000000?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/Windows-000000?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
<img src="https://img.shields.io/badge/Linux-000000?style=for-the-badge&logo=linux&logoColor=white" alt="Linux" />

</div>

---

Toolkit de diagnóstico para suporte e infraestrutura com CLI e dashboard web.

## Recursos

- CPU, memória e uptime;
- inventário de discos;
- interfaces de rede;
- teste de conectividade externa;
- teste de DNS;
- processos com maior consumo;
- recomendações baseadas em limiares;
- exportação de relatório JSON;
- dashboard web;
- operação somente leitura.

## CLI

~~~bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python support_toolkit.py --report reports/diagnostic.json
~~~

## Dashboard

~~~bash
uvicorn web_app:app --reload
~~~

Acesse <code>http://127.0.0.1:8000</code>.

## Testes

~~~bash
python -m pytest -q
~~~

## Segurança

O toolkit não altera registro, firewall, usuários, políticas ou configurações do sistema. A proposta é coletar evidências antes de qualquer ação corretiva.

---

<div align="center">

Diagnosticar primeiro. Reiniciar “pra ver se volta” depois.

</div>
