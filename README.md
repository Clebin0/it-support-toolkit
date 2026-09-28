# IT Support Toolkit

Ferramentas de diagnóstico para suporte e infraestrutura Windows, desenvolvidas em Python.

## Recursos
- Coleta de informações do sistema, CPU, memória e discos
- Testes de DNS, gateway e conectividade
- Inventário de interfaces de rede
- Verificação de serviços críticos
- Exportação de relatório JSON
- CLI segura: somente leitura por padrão

## Uso
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python support_toolkit.py --report report.json
```

## Segurança
O projeto não altera registro, firewall, usuários ou políticas. Foi pensado para diagnóstico antes de qualquer ação corretiva.

## Stack
Python 3.11+ · psutil · stdlib

## Roadmap
Interface web, histórico de diagnósticos, testes automatizados adicionais e integração opcional com inventário.

MIT License.