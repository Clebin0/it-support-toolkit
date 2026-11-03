# Segurança

O IT Support Toolkit foi concebido para coletar informações sem modificar a configuração da estação.

## Escopo

O programa lê métricas expostas pelo sistema operacional, interfaces de rede, discos montados, DNS e metadados de processos. Não altera registro, firewall, contas, serviços, drivers ou políticas.

## Exposição do dashboard

A aplicação FastAPI não implementa autenticação. Por isso, o servidor deve permanecer ligado a `127.0.0.1` durante o uso local. Não use `--host 0.0.0.0` em redes compartilhadas ou públicas sem adicionar autenticação, controle de acesso e proteção de transporte.

## Dados coletados

Relatórios podem conter hostname, IPs locais, nomes de processos, PIDs, uso de recursos e nomes de volumes. Trate arquivos JSON como informação interna e revise o conteúdo antes de compartilhar.

## Relato de problema

Não abra uma issue pública com IPs, nomes de máquinas, nomes de usuários, logs ou relatórios reais. Remova esses dados antes de enviar uma reprodução mínima.
