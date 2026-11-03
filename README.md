# IT Support Toolkit

Ferramenta de diagnóstico para suporte e infraestrutura. Reúne informações de uma estação antes de iniciar alterações: recursos, armazenamento, rede, resolução DNS e processos em execução.

A coleta é somente leitura. O relatório ajuda a registrar o estado observado e a organizar a próxima etapa do troubleshooting; não tenta corrigir o computador automaticamente.

## O que coleta

- CPU: quantidade de núcleos lógicos/físicos e uso no instante da coleta.
- Memória: total, disponível e percentual utilizado.
- Sistema: hostname, plataforma e horário de inicialização.
- Discos: dispositivo, ponto de montagem, capacidade e espaço livre.
- Rede: endereços associados às interfaces.
- Conectividade: teste de alcance a um IP externo e resolução DNS.
- Processos: processos visíveis com maior uso de CPU e memória.
- Recomendações: alertas simples baseados em limiares explícitos.
- Relatório JSON para anexar ao chamado ou comparar com uma coleta posterior.

## Executar

Requer Python 3.12 ou superior.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Coleta e exibe o relatório
python support_toolkit.py

# Salva uma cópia em JSON
python support_toolkit.py --report reports/diagnostic.json

# Saída compacta para integração com outros scripts
python support_toolkit.py --compact
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python support_toolkit.py --report reports/diagnostic.json
```

## Dashboard local

```powershell
uvicorn web_app:app --host 127.0.0.1 --port 8000
```

Abra [http://127.0.0.1:8000](http://127.0.0.1:8000). O dashboard executa uma nova coleta quando solicitado; ele não consulta os dados salvos no último relatório.

O endpoint `GET /health` informa a versão da API. `GET /diagnostic` executa a coleta e devolve o JSON.

## Docker

```bash
docker build -t it-support-toolkit .
docker run --rm -p 127.0.0.1:8000:8000 it-support-toolkit
```

A imagem é útil para executar o dashboard num ambiente controlado. Para inspecionar a máquina host, lembre-se de que um container normalmente enxerga o próprio ambiente isolado, não todos os recursos do host.

## Testes

```bash
python -m pytest -q
```

A suíte cobre o formato do relatório, resolução DNS, recomendações e endpoint de saúde. A execução de CI usa Python 3.12.

## Como interpretar os resultados

O percentual de CPU é uma amostra do momento da coleta. O primeiro valor de CPU por processo pode ser zero porque o sistema ainda não tem intervalo suficiente para calcular a utilização. Uma falha de ping não prova que a internet caiu: o destino pode bloquear ICMP. Falha de DNS deve ser analisada junto do servidor configurado e do contexto da rede.

As recomendações são regras simples, não diagnóstico definitivo. Um disco acima de 90% pode justificar limpeza planejada, mas a ferramenta não apaga arquivos nem escolhe o que remover.

## Segurança e privacidade

- A ferramenta não altera registro, firewall, usuários, serviços, drivers, políticas ou configurações.
- A lista de processos e os endereços de rede podem conter informação sensível. Revise o JSON antes de anexar ou compartilhar.
- O dashboard não possui autenticação. Mantenha-o em loopback (`127.0.0.1`) ou proteja-o com uma camada de autenticação/rede confiável antes de expor.
- Evite executar o serviço em `0.0.0.0` numa rede pública ou corporativa sem controles de acesso.
- O resultado depende das permissões do usuário e do sistema operacional.

## Limitações conhecidas

Não recolhe logs do Windows Event Viewer ou journald, estado de serviços, drivers, SMART detalhado, latência contínua, Wi-Fi por SSID, inventário de software nem telemetria histórica. Também não faz correlação entre eventos. Essas informações podem ser adicionadas em módulos separados, mantendo o princípio de coleta sem alteração.

## Estrutura

- `support_toolkit.py`: coleta, regras e interface de linha de comando.
- `web_app.py`: API FastAPI.
- `frontend.html`: dashboard.
- `tests/`: testes automatizados.
- `docs/ARCHITECTURE.md`: fluxo de coleta e limites.

---

Feito para uma rotina simples: registrar primeiro, entender o cenário e só então decidir a correção.
