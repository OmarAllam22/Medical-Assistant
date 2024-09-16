#!/bin/bash
pip install requirements.txt
chmod +x main_script.sh
python tools/create_vectordb.py
python tools/get_books_info.py
