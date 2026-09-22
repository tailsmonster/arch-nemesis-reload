#!/usr/bin/env bash
set -euo pipefail

cd backend
micromamba env create -f environment.yml || micromamba env update -f environment.yml
micromamba run -n arch-nemesis-reload-backend uvicorn arch_nemesis.main:app --reload
