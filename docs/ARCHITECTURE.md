# Architecture

## Goal

IT Support Toolkit collects diagnostic evidence before corrective action. The project is intentionally read-only.

## Flow

```mermaid
flowchart LR
    A[Local machine] --> B[Diagnostic collectors]
    B --> C[CPU / memory / uptime]
    B --> D[Disk inventory]
    B --> E[Network / DNS]
    B --> F[Process usage]
    C --> G[Normalized diagnostic report]
    D --> G
    E --> G
    F --> G
    G --> H[Rule-based recommendations]
    G --> I[JSON export]
    G --> J[FastAPI dashboard]
```

## Design principle

Evidence comes before remediation. The toolkit does not modify registry settings, firewall rules, local users, policies or system configuration.

## Production evolution

Future versions can add signed reports, remote collection through an authenticated agent, structured incident bundles, inventory correlation and integrations with monitoring or ITSM systems.
