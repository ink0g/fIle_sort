"""
Умная сортировка файлов
- Выбор папки
- Сортировка по расширению или по дате
- Автоматическое создание папок
- Лог в консоль: что куда перенесено
"""

import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_TK = True
except ImportError:
    HAS_TK = False


def select_folder():
    """Открывает диалог выбора папки."""
    if HAS_TK:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Выберите папку для сортировки")
        root.destroy()
        return folder
    else:
        return input("Введите путь к папке: ").strip().strip('"')


def sort_by_extension(folder_path):
    """Сортировка файлов по расширению."""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print("Ошибка: папка не существует или недоступна.")
        return 0

    files_by_ext = defaultdict(list)
    moved_count = 0

    for item in folder.iterdir():
        if item.is_file():
            ext = item.suffix.lower() or "_без_расширения"
            ext = ext.lstrip(".") if ext != "_без_расширения" else ext
            files_by_ext[ext].append(item)

    for ext, files in files_by_ext.items():
        subfolder_name = ext if ext != "_без_расширения" else "без_расширения"
        subfolder = folder / subfolder_name
        subfolder.mkdir(exist_ok=True)

        for file_path in files:
            dest = subfolder / file_path.name
            try:
                shutil.move(str(file_path), str(dest))
                print(f"  {file_path.name} -> {subfolder_name}/")
                moved_count += 1
            except Exception as e:
                print(f"  Ошибка: {file_path.name} - {e}")

    return moved_count


def sort_by_date(folder_path):
    """Сортировка файлов по дате создания/модификации."""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print("Ошибка: папка не существует или недоступна.")
        return 0

    files_by_date = defaultdict(list)

    for item in folder.iterdir():
        if item.is_file():
            mtime = item.stat().st_mtime
            date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            files_by_date[date_str].append(item)

    moved_count = 0
    for date_str, files in files_by_date.items():
        subfolder = folder / date_str
        subfolder.mkdir(exist_ok=True)

        for file_path in files:
            dest = subfolder / file_path.name
            try:
                shutil.move(str(file_path), str(dest))
                print(f"  {file_path.name} -> {date_str}/")
                moved_count += 1
            except Exception as e:
                print(f"  Ошибка: {file_path.name} - {e}")

    return moved_count


def main():
    print("=" * 50)
    print("  Умная сортировка файлов")
    print("=" * 50)

    folder = select_folder()
    if not folder:
        print("Папка не выбрана. Выход.")
        return

    print(f"\nПапка: {folder}\n")

    print("Режим сортировки:")
    print("  1 - По расширению (jpg, png, mp4, pdf и т.д.)")
    print("  2 - По дате создания")
    choice = input("Выберите (1 или 2): ").strip() or "1"

    print("\n--- Лог переносов ---\n")

    if choice == "2":
        count = sort_by_date(folder)
    else:
        count = sort_by_extension(folder)

    print(f"\n--- Готово. Перенесено файлов: {count} ---")


if __name__ == "__main__":
    main()
