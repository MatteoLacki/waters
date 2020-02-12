import platform

if platform.system() == 'Windows':
    try: # get a shortcut in Sendto:
        import sys
        import os
        from pathlib import Path
        from pprint import pprint
        scripts_path = Path(sys.prefix)/'Scripts'
        sendto_path = Path(*scripts_path.parts[:4])/"Roaming"/"Microsoft"/"Windows"/"SendTo"
        iadbs2stats = sendto_path/"_iadbs2stats.py"
        if not iadbs2stats.exists():
            os.link(scripts_path/"iadbs2stats.py", iadbs2stats)
        iadbs2csv = sendto_path/"_iadbs2csv.py"
        if not iadbs2csv.exists():
            os.link(scripts_path/"iadbs2csv.py", iadbs2csv)
    except Exception as e:
        print(e)
        pass


print('Created scripts.')
input()