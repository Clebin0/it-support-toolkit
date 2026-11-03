# Segurança

O IT Support Toolkit foi concebido para coletar informações sem modificar a configuração da estação.

## Escopo

O programa lê métricas expostas pelo sistema operacional, interfaces de rede, discos montados, DNS e metadados de processos. Não altera registro, firewall, contas, serviços, drivers ou políticas.

## Proteção do dashboard

A aplicação FastAPI não implementa autenticação de usuário. Para reduzir o risco de exposição acidental, toda requisição é bloqueada quando o endereço do cliente não é loopback. O middleware também restringe o cabeçalho `Host` a `localhost`, `127.0.0.1` e `[::1]`.

Execute sempre com:

```powershell
uvicorn web_app:app --host 127.0.0.1 --port 8000
```

Não publique a porta, não use `--host 0.0.0.0` e não coloque o dashboard atrás de um proxy reverso público. O bloqueio de loopback é uma defesa adicional, não substitui autenticação para uma instalação multiusuário.

## Dados coletados

Relatórios podem conter hostname, IPs locais, nomes de processos, PIDs, uso de recursos e nomes de volumes. Trate arquivos JSON como informação interna e revise o conteúdo antes de compartilhar.

## Relato de problema

Não abra uma issue pública com IPs, nomes de máquinas, nomes de usuários, logs ou relatórios reais. Remova esses dados antes de enviar uma reprodução mínima.
