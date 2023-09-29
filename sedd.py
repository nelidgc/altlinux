#!/usr/bin/python3

import json
import os


path_google_chrome = os.path.expanduser(r'~/.config/google-chrome/NativeMessagingHosts')
browsers = ['chromium', 'yandex-browser', 'chromium-gost']
upd_dict = {'newAllowFileAccess':True, 'incognito':True}

  
os.system(f"""
cd ~
wget -P ~/ http://cm.nso.ru:8080/cmj-web/plugin2/cmjproxyplugin2_x64.run
chmod +rwx cmjproxyplugin2_x64.run
./cmjproxyplugin2_x64.run
rm -f cmjproxyplugin2_x64.run
""")
try:
    for browser in browsers:
        path_browser = os.path.expanduser(f'~/.config/{browser}/')
        os.system(f'cp -r {path_google_chrome} {path_browser}')

    for browser in browsers:
        path_json = os.path.expanduser(f'~/.config/{browser}/Default/Preferences')
        with open(path_json, 'r') as f:
            string = json.load(f)

        with open(path_json, "w") as f:
            key = string['extensions']['settings']['dpkefahlefbmfgfgfoppbpkacgdmadpp']
            key.update(upd_dict)
            f.write(json.dumps(string))
    print("\nВсе прошло успешно!")        
except FileNotFoundError:
    print(f"\nЗапустите, потом завершите работу {browser} и повторите запуск скрипта!")
