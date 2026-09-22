#!/usr/bin/env bash
set -euo pipefail

cd backend
micromamba run -n arch-nemesis-reload-backend pytest
