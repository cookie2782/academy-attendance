# -*- coding: utf-8 -*-
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.chdir(current_dir)

# main.py 실행
if __name__ == "__main__":
    import main

