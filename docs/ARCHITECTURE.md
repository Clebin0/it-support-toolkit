# Arquitetura

A proposta do toolkit é coletar informação antes de sair alterando configuração da máquina.

```mermaid
flowchart LR
    A[Máquina] --> B[Coleta]
    B --> C[CPU / memória / uptime]
    B --> D[Discos]
    B --> E[Rede / DNS]
    B --> F[Processos]
    C --> G[Relatório]
    D --> G
    E --> G
    F --> G
    G --> H[Recomendações]
    G --> I[JSON]
    G --> J[Dashboard]
```

A coleta é somente leitura. O projeto não altera registro, firewall, usuários ou políticas do Windows.

A ideia é usar o relatório como ponto de partida para troubleshooting, em vez de executar correções automáticas sem saber primeiro o que está acontecendo.
