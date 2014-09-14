#!/usr/bin/env bash
#~/Envs/venv_recipes/bin/python runp.py
~/Envs/venv_recipes/bin/gunicorn -b 0.0.0.0:5100 app:app
