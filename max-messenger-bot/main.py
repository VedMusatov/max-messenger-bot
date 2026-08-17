#!/usr/bin/env python3
"""
Max Messenger Bot - Главный запускной файл
"""

import sys
import os
import logging

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.bot import main

if __name__ == "__main__":
    # Запускаем бота
    exit_code = main()
    sys.exit(exit_code)