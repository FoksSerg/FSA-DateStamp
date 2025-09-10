# batch_processor.py - для обработки нескольких папок
import os
import subprocess
import sys

def process_multiple_folders(root_folder, output_base=None):
    """Обработка всех подпапок с изображениями"""
    
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        
        if os.path.isdir(folder_path):
            if output_base:
                output_folder = os.path.join(output_base, folder_name)
                os.makedirs(output_folder, exist_ok=True)
            else:
                output_folder = None
            
            print(f"Обработка папки: {folder_name}")
            
            cmd = [
                sys.executable, 'DateStamp.py',
                folder_path,
                '-o', output_folder if output_folder else folder_path,
                '--font-size', '35',
                '--position', 'bottom-right'
            ]
            
            subprocess.run(cmd)

def process_with_structure_preservation(source_root, dest_root):
    """Обработка с сохранением структуры папок и метаданных"""
    
    print(f"Обработка с сохранением структуры:")
    print(f"Исходная папка: {source_root}")
    print(f"Папка назначения: {dest_root}")
    
    cmd = [
        sys.executable, 'DateStamp.py',
        source_root,
        '-o', dest_root,
        '--preserve-structure',
        '--font-size', '35',
        '--position', 'bottom-right'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Обработка завершена успешно!")
        print(result.stdout)
    else:
        print("Ошибка при обработке:")
        print(result.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_root = sys.argv[1]
        output_root = sys.argv[2] if len(sys.argv) > 2 else None
        
        # Проверяем, есть ли флаг для сохранения структуры
        if len(sys.argv) > 3 and sys.argv[3] == '--preserve-structure':
            if not output_root:
                print("Ошибка: Для режима сохранения структуры необходимо указать папку вывода")
                sys.exit(1)
            process_with_structure_preservation(input_root, output_root)
        else:
            process_multiple_folders(input_root, output_root)
    else:
        print("Использование:")
        print("  python PacketFolder.py /путь/к/папкам [/путь/для/результатов]")
        print("  python PacketFolder.py /путь/к/папкам /путь/для/результатов --preserve-structure")