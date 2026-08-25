<p align="center">
  <img src="assets/header.svg" alt="Luca Filippin — Backend engineer. Twenty-five years in Go, Python, C and C++" width="100%">
</p>

<p align="center">
  <a href="https://linkedin.com/in/luca-f-5148692"><img src="https://img.shields.io/badge/LinkedIn-24292f?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0yMC40NDcgMjAuNDUyaC0zLjU1NHYtNS41NjljMC0xLjMyOC0uMDI3LTMuMDM3LTEuODUyLTMuMDM3LTEuODUzIDAtMi4xMzYgMS40NDUtMi4xMzYgMi45Mzl2NS42NjdIOS4zNTFWOWgzLjQxNHYxLjU2MWguMDQ2Yy40NzctLjkgMS42MzctMS44NSAzLjM3LTEuODUgMy42MDEgMCA0LjI2NyAyLjM3IDQuMjY3IDUuNDU1djYuMjg2ek01LjMzNyA3LjQzM2MtMS4xNDQgMC0yLjA2My0uOTI2LTIuMDYzLTIuMDY1IDAtMS4xMzguOTItMi4wNjMgMi4wNjMtMi4wNjMgMS4xNCAwIDIuMDY0LjkyNSAyLjA2NCAyLjA2MyAwIDEuMTM5LS45MjUgMi4wNjUtMi4wNjQgMi4wNjV6bTEuNzgyIDEzLjAxOUgzLjU1NVY5aDMuNTY0djExLjQ1MnpNMjIuMjI1IDBIMS43NzFDLjc5MiAwIDAgLjc3NCAwIDEuNzI5djIwLjU0MkMwIDIzLjIyNy43OTIgMjQgMS43NzEgMjRoMjAuNDUxQzIzLjIgMjQgMjQgMjMuMjI3IDI0IDIyLjI3MVYxLjcyOUMyNCAuNzc0IDIzLjIgMCAyMi4yMjUgMHoiLz48L3N2Zz4=" alt="LinkedIn"></a>
  <a href="https://gitlab.com/lucafilippin"><img src="https://img.shields.io/badge/GitLab-24292f?style=flat-square&logo=gitlab&logoColor=white" alt="GitLab"></a>
  <a href="mailto:luca.filippin@gmail.com"><img src="https://img.shields.io/badge/Email-24292f?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>
</p>

---

Most of my work has gone into distributed systems and backend services: job
schedulers running across six operating systems, REST APIs on Kubernetes,
cryptographic key storage on encryption hardware, a 250,000-line C port from
Mac OS 9 to Mac OS X.

Lately I build agentic tooling and MCP services for my own workflow — navigating
large codebases, driving multi-step refactors, catching defects before review.

### Toolbox

| Languages | Infrastructure | Observability &amp; data |
| :---: | :---: | :---: |
| <img src="https://img.shields.io/badge/Go-24292f?style=flat-square&logo=go&logoColor=white" alt="Go"> <img src="https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/C-24292f?style=flat-square&logo=c&logoColor=white" alt="C"> <img src="https://img.shields.io/badge/C%2B%2B-24292f?style=flat-square&logo=cplusplus&logoColor=white" alt="C++"> | <img src="https://img.shields.io/badge/Kubernetes-30363d?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes"> <img src="https://img.shields.io/badge/Docker-30363d?style=flat-square&logo=docker&logoColor=white" alt="Docker"> <img src="https://img.shields.io/badge/Helm-30363d?style=flat-square&logo=helm&logoColor=white" alt="Helm"> <img src="https://img.shields.io/badge/Jenkins-30363d?style=flat-square&logo=jenkins&logoColor=white" alt="Jenkins"> | <img src="https://img.shields.io/badge/Prometheus-424a53?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus"> <img src="https://img.shields.io/badge/Grafana-424a53?style=flat-square&logo=grafana&logoColor=white" alt="Grafana"> <img src="https://img.shields.io/badge/PostgreSQL-424a53?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"> |

---

### Open source

#### [NTPSync](https://github.com/lucaf/NTPSync) &nbsp;<sub>C · Python</sub>

An NTP client: C library with a Python wrapper, Linux and macOS. It grew out of a
client I wrote for an fNIRS acquisition system that needed several machines
agreeing on time to within a millisecond.

#### [Structured decoding errors for mapstructure](https://github.com/mitchellh/mapstructure/pull/331) &nbsp;<sub>Go</sub>

A `Namespace` type that records the full field path where decoding failed, with
source and destination values and error kinds, so a failure three levels into a
nested config says where it happened.

<details>
<summary>What it adds</summary>

- `Namespace` and `NamespaceFld` — hierarchical error location by field name or tag
- `LocalizedError` interface and `AsDecodingErrors()`
- Error kinds, and a refactor of error handling across the codebase

Nine commits. Still open when the project was archived in July 2024;
[go-viper/mapstructure](https://github.com/go-viper/mapstructure) is the successor.

</details>

#### [career-ai-agent](https://github.com/lucaf/career-ai-agent) &nbsp;<sub>Python</sub>

A service that answers questions about a professional history, grounded in supplied
documents. Pluggable LLM providers, streaming responses, remote profile storage so
source material never enters the repository.

#### [WTools](https://github.com/cogdevtools/WTools) &nbsp;<sub>MATLAB</sub>

A toolbox for time-frequency analysis of infant EEG. I rewrote it between October
2023 and June 2024 — 116 commits merged as v2.0, fourteen merged pull requests
since 2023.

<details>
<summary>What the rewrite covered</summary>

- The logging, project and utility core
- Channel location and spline handling, with Cz restore for EGI layouts
- Precise time-domain computation for Morlet wavelets, with FWHM reported so the
  time–frequency tradeoff is stated rather than assumed
- Baseline normalisation, dB plots, colorbar ranges
- Export of CWT real and imaginary components; single-header TSV output

</details>

Described in Ferrari A., **Filippin L.**, Buiatti M., Parise E. (2025),
*WTools: a MATLAB-based toolbox for time-frequency analysis of infant data.*

---

### Activity

<p align="center">
  <img src="https://raw.githubusercontent.com/lucaf/lucaf/metrics/metrics.calendar.svg" alt="Contribution calendar" width="52%">
  <img src="https://raw.githubusercontent.com/lucaf/lucaf/metrics/contributions.svg" alt="Contribution breakdown" width="42%">
</p>
