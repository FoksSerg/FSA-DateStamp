#!/usr/bin/env python3
"""
Тестовый скрипт для проверки определения версии Windows
"""

import platform
import sys

# Импорт winreg только на Windows
if platform.system() == 'Windows':
    import winreg

def get_windows_version():
    """Определение версии Windows для выбора стратегии сборки"""
    try:
        if platform.system() != 'Windows':
            return 'unknown'
        
        # Сначала проверяем platform.platform() - это самый надежный способ
        platform_info = platform.platform()
        release = platform.release()
        
        print(f"Platform: {platform_info}")
        print(f"Release: {release}")
        
        # Приоритет: platform.platform() для Windows 11
        if 'Windows-11' in platform_info or 'windows-11' in platform_info.lower():
            print("✅ Определено как Windows 11 по platform.platform()")
            return 'windows11'
        
        # Получаем версию Windows из реестра для остальных случаев
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            version, _ = winreg.QueryValueEx(key, "CurrentVersion")
            build_number, _ = winreg.QueryValueEx(key, "CurrentBuild")
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            winreg.CloseKey(key)
            
            print(f"Registry version: {version}")
            print(f"Build number: {build_number}")
            print(f"Product name: {product_name}")
            
            # Определяем версию по номеру и build number
            if version.startswith('6.1'):
                return 'windows7'
            elif version.startswith('6.2'):
                return 'windows8'
            elif version.startswith('6.3'):
                return 'windows8_1'
            elif version.startswith('10.0'):
                # Windows 10 vs Windows 11 по build number и названию продукта
                try:
                    build = int(build_number)
                    product_lower = product_name.lower()
                    
                    print(f"Build as int: {build}")
                    print(f"Product lower: {product_lower}")
                    
                    # Проверяем название продукта для Windows 11
                    if 'windows 11' in product_lower or build >= 22000:
                        return 'windows11'
                    else:  # Windows 10
                        return 'windows10'
                except ValueError:
                    return 'windows10'  # Fallback
            else:
                return 'windows11'
                
        except Exception as e:
            print(f"Ошибка чтения реестра: {str(e)}")
            # Fallback - используем platform.release()
            if release == '7':
                return 'windows7'
            elif release == '8':
                return 'windows8'
            elif release == '8.1':
                return 'windows8_1'
            elif release == '10':
                return 'windows10'
            else:
                return 'windows11'
                
    except Exception as e:
        print(f"Не удалось определить версию Windows: {str(e)}")
        return 'unknown'

if __name__ == "__main__":
    print("=== Тест определения версии Windows ===")
    print(f"Platform: {platform.platform()}")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print()
    
    version = get_windows_version()
    print(f"Определенная версия: {version}")
    
    # Определяем папку
    if version == 'windows7':
        folder = 'Windows7'
    elif version in ['windows8', 'windows8_1']:
        folder = 'Windows8'
    elif version == 'windows10':
        folder = 'Windows10'
    elif version == 'windows11':
        folder = 'Windows11'
    else:
        folder = 'Universal'
    
    print(f"Папка для сборки: {folder}")
