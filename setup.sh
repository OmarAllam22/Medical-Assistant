#!/bin/bash
pip install -r requirements.txt
chmod +x main_script.sh
python utils/create_vectordb.py
python utils/get_books_info.py
