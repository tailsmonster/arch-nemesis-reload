#!/usr/bin/env bash
set -euo pipefail

cd backend
micromamba run -n arch-nemesis-reload-backend python -m arch_nemesis.evals.runner
