# CloudPilot ⚙️

> **Automated CI/CD orchestration for AWS-native teams.**
> Ship faster, deploy safer, and stop babysitting pipelines.

[![Build Status](https://img.shields.io/github/actions/workflow/status/ayushsingh/cloudpilot/ci.yml?branch=main)](https://github.com/ayushsingh/cloudpilot/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ayushsingh/cloudpilot)](https://github.com/ayushsingh/cloudpilot/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📌 Overview

**CloudPilot** is a lightweight orchestration layer that sits between your codebase and AWS, automating the repetitive parts of deployment: infrastructure provisioning, container builds, and rollout verification. It was built to eliminate the copy-pasted bash scripts and half-documented runbooks that quietly run production systems everywhere.

Whether you're managing a single EC2 fleet or a multi-service Kubernetes setup, CloudPilot gives you one consistent interface to plan, deploy, and roll back changes — with guardrails baked in.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker 24+
- AWS CLI v2, configured with valid credentials
- Terraform 1.6+ (optional, for infra provisioning)

### Installation

```bash
# Clone the repository
git clone https://github.com/ayushsingh/cloudpilot.git
cd cloudpilot

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example config and fill in your values
cp config.example.yaml config.yaml
```

```yaml
# config.yaml
aws:
  region: ap-south-1
  profile: default
pipeline:
  environments: [dev, staging, prod]
  approval_required: [prod]
```

### Run It

```bash
# Validate your configuration
cloudpilot validate

# Deploy to an environment
cloudpilot deploy --env staging

# Roll back the last deployment
cloudpilot rollback --env staging --steps 1
```

---

## ✨ Features

- **One-command deployments** — provision, build, and ship without juggling five different tools.
- **Environment-aware pipelines** — separate configs for dev/staging/prod with optional manual approval gates.
- **Automatic rollback** — failed health checks trigger an automatic revert to the last known-good state.
- **Infrastructure as Code** — native Terraform integration for reproducible AWS environments.
- **Pluggable notifications** — Slack, email, or webhook alerts on deploy success/failure.
- **Dry-run mode** — preview exactly what will change before anything touches production.

---

## 🛠️ Tech Stack

| Layer            | Technology                          |
|------------------|--------------------------------------|
| Core language    | Python 3.10+                        |
| Containerization | Docker                               |
| Infrastructure   | Terraform, AWS (EC2, S3, Lambda, VPC)|
| CI/CD            | GitHub Actions, Jenkins (optional)   |
| Orchestration    | Kubernetes (optional)                |
| Monitoring       | AWS CloudWatch                       |

---

## 🧪 Usage Example

```python
from cloudpilot import Pipeline

pipeline = Pipeline(config="config.yaml")

# Plan a deployment without applying it
plan = pipeline.plan(env="prod")
print(plan.summary())

# Execute if the plan looks good
if plan.is_safe():
    pipeline.deploy(env="prod")
```

```bash
$ cloudpilot deploy --env prod --dry-run
✔ Validating configuration
✔ Building container image (v1.4.2)
✔ Provisioning infrastructure changes (2 resources)
✔ Running pre-deploy health checks
→ Dry run complete. No changes applied.
```

---

## 🤝 Contributing

Contributions are welcome and appreciated — this project grows better with more perspectives.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: short description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request describing your changes and why they matter

**Guidelines:**
- Follow existing code style (PEP 8 for Python).
- Include tests for new functionality.
- Keep PRs focused — one feature or fix per PR.
- Update documentation alongside code changes.

Found a bug or have a feature request? [Open an issue](https://github.com/ayushsingh/cloudpilot/issues).

---

## 🗺️ Roadmap

- [ ] Multi-cloud support (GCP, Azure)
- [ ] Web dashboard for deployment history and metrics
- [ ] Built-in secrets management via AWS Secrets Manager
- [ ] Canary and blue-green deployment strategies
- [ ] Plugin SDK for custom deployment steps

Have an idea? Suggestions are always welcome via issues or discussions.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ayush Singh**
DevOps & Cloud Infrastructure Engineer, based in Bengaluru, India

Focused on CI/CD automation, AWS infrastructure, and building tools that make deployments boring (in the best way). Background in Java, Python, and JavaScript, with hands-on experience across EC2, S3, Lambda, VPC, CloudWatch, Docker, Kubernetes, Jenkins, and Terraform.

- 💼 GitHub: [github.com/ayushsingh](https://github.com/ayushsingh)
- 📧 Email: your.email@example.com
- 🔗 LinkedIn: [linkedin.com/in/ayushsingh](https://linkedin.com/in/ayushsingh)

---

## 📚 Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

<p align="center">If this project saves you time, consider giving it a ⭐ — it helps others find it too.</p>
