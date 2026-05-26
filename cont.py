import os
import re

TARGET_DIR = 'Code'
TXT_FILE = 'cont.txt'
README_FILE = 'README.md'

def cont(directory):
    total = 0
    # os.walk 會幫我們自動遞迴走訪所有子資料夾
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 只計算 .cpp 檔案
            if file.endswith('.cpp'):
                total += 1
    return total

if __name__ == '__main__':
    if os.path.exists(TARGET_DIR):
        count = cont(TARGET_DIR)
        
        # 1. 寫入純數字到 cont.txt
        with open(TXT_FILE, 'w', encoding='utf-8') as f:
            f.write(str(count))
            
        # 2. 更新 README.md 裡面的徽章數字
        if os.path.exists(README_FILE):
            with open(README_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正規表達式找出徽章並替換數字
            badge_pattern = r'(https://img\.shields\.io/badge/目前總題數-)\d+(-blue)'
            new_content = re.sub(badge_pattern, rf'\g<1>{count}\g<2>', content)
            
            with open(README_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)