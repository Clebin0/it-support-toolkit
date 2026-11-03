# Arquitetura

O toolkit separa coleta, interpretação e apresentação. O mesmo relatório é usado pela CLI e pelo dashboard, evitando duas implementações diferentes de diagnóstico.

```mermaid
flowchart TD
    A[Estação local] --> B[psutil e APIs do sistema]
    B --> C[CPU, memória e uptime]
    B --> D[Discos e interfaces]
    B --> E[Processos]
    F[ICMP e DNS] --> G[Conectividade]
    C --> H[Relatório normalizado]
    D --> H
    E --> H
    G --> H
    H --> I[Regras de atenção]
    I --> J[CLI JSON]
    I --> K[FastAPI /diagnostic]
    K --> L[Dashboard local]
```

## Módulos

- `support_toolkit.py`: funções de coleta, formatação do relatório e CLI.
- `web_app.py`: camada HTTP. Devolve mensagem genérica ao navegador quando a coleta falha e guarda detalhes no log local.
- `frontend.html`: apresentação dos dados devolvidos pela API.

## Coleta e limites

A utilização de CPU é amostrada durante a execução. O uso de processos exige duas leituras separadas por um pequeno intervalo; processos encerrados durante essa janela são ignorados. Volumes sem permissão de leitura são omitidos.

O teste ICMP consulta um endereço externo uma única vez. Firewalls podem bloquear esse tipo de pacote. A resolução DNS usa o resolvedor configurado no sistema. Nenhum dos dois resultados, isoladamente, determina a causa de uma falha de rede.

## Segurança

O dashboard não possui autenticação e deve ficar em loopback. Os relatórios podem conter endereços, hostname, processos e pontos de montagem. A aplicação não altera configurações, mas ainda assim os dados coletados devem ser tratados com cuidado.
