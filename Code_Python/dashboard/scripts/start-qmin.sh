#!/bin/bash
set -xe
gunicorn app:server --bind=0.0.0.0:8000 --timeout=300