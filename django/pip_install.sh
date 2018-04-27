#!/bin/bash

pip install -r requirements.txt
pip uninstall psycopg2    
pip install --no-binary :all: psycopg2

