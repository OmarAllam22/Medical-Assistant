#!/bin/bash
pip install requirements.txt
chmod +x main_script.sh
python create_vectordb.py
python get_books_info.py
