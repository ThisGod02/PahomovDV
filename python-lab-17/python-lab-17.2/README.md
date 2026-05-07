# Lab 17.2 - CI/CD Pack

This folder contains the CI/CD and IaC layer for the deployed stack from `../python-lab-17.1`.

Contents:
- `.github/workflows/deploy.yml` - GitHub Actions pipeline
- `terraform/` - starter infrastructure as code for Yandex Cloud

The workflow is intentionally scaffolded with secrets-based configuration so it can be adapted on GitHub without hardcoding credentials.
