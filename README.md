# IT Support Toolkit

Toolkit de diagnostico para suporte e infraestrutura, com CLI e dashboard web.

## Recursos

- CPU, memoria e uptime
- Inventario de discos
- Interfaces de rede
- Teste de conectividade externa
- Teste de DNS
- Processos com maior consumo
- Recomendacoes basicas baseadas em limiares
- Exportacao de relatorio JSON
- Dashboard web
- Operacao somente leitura

## CLI

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python support_toolkit.py --report reports/diagnostic.json
```

## Dashboard

```bash
uvicorn web_app:app --reload
```

Abra http://127.0.0.1:8000.

## Testes

```bash
python -m pytest -q
```

## Seguranca

O projeto nao altera registro, firewall, usuarios, politicas ou configuracoes do sistema. A proposta e coletar evidencias antes de qualquer acao corretiva.
