# Multi-agent architecture

## Roles

- **Diagnostic interpreter**: explains the existing JSON report and differentiates measurements from hypotheses.
- **Network analyst**: interprets DNS/connectivity observations with known ICMP and resolver limitations.
- **Windows/Linux runbook advisor**: provides safe, reversible diagnostic steps tailored to the reported platform.
- **Privacy reviewer**: identifies process names, hostnames, IP addresses, and other fields that should be redacted before sharing.
- **Report writer**: prepares a ticket-ready summary with facts, hypotheses, and next checks separated.

## Boundaries

The toolkit's current read-only collection contract is preserved. Agents cannot change registry, firewall, users, services, drivers, policies, files, or network configuration. The unauthenticated dashboard remains loopback-only until authentication exists. Agent endpoints must not expose reports to unauthenticated remote callers.

## Acceptance

Recommendations identify which report fields support them, acknowledge sampling limitations, and never present simple threshold rules as definitive diagnosis.
