#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Exécuter Flake8
flake8 .

# Exécuter Black
black --check .
