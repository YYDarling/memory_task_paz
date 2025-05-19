# === main.py ===
from task import run_task
import os
import psychopy
psychopy.prefs.general['winType'] = 'pyglet'
import sys
import signal

from psychopy import logging

# 🔧 禁用所有 console 输出和写入日志文件
logging.console = None




def clean_exit(app):
    try:
        app.Destroy()
    except:
        pass
    from psychopy import core
    import os, signal, sys
    core.quit()
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(0)


if __name__ == '__main__':
    from config import config
    from psychopy import gui, core
    import wx
    from psychopy import logging
    logging.console = None  # ✅ 禁用日志写入 console，防止退出时崩溃

    app = wx.App(False)  # ✅ 始终创建 app 对象

    while True:
        print("🟢 main.py running")  # ✅ 启动标志


        # GUI dialog for subject ID and session number
        dlg = gui.Dlg(title="Memory Task Setup")
        dlg.addField('Subject Group (e.g., control, hip):', "control")
        dlg.addField('Subject ID (e.g.,sub01):', "sub01")
        dlg.addField('Session Number (e.g.,1):', "1")
        dlg.addField('Task Mode:', choices=['self_paced', 'fixed'], initial='self-paced')
        
        try:
            ok_data = dlg.show()
        except Exception as e:
            print(f"❌ Dialog error: {e}")
            clean_exit(app)


        if not dlg.OK:
            print("❌ User canceled the dialog. Exiting...")
            clean_exit(app)


        if dlg.OK:
            subject_group = ok_data[0]
            subject_id = ok_data[1]
            session_num = ok_data[2]
            config['mode'] = ok_data[3]

            
        else:
            core.quit()


        subj_folder = os.path.join(config['output_base'], f"{subject_group}", f"{subject_id}")
        session_file = os.path.join(subj_folder, f"session_{session_num}_{config['mode']}.csv")

        if not os.path.exists(subj_folder):
            os.makedirs(subj_folder)

        print(f"📂 Checking if session file exists at: {session_file}")

        if os.path.exists(session_file):
            overwrite_dlg = gui.Dlg(title="Overwrite Warning")
            overwrite_dlg.addText(f"Session file already exists:\n{session_file}")
            overwrite_dlg.addText("Overwrite this session?")
            overwrite_dlg.addField('Overwrite?', choices=["No", "Yes"])

            try:
                response = overwrite_dlg.show()
            except Exception as e:
                print(f"❌ Overwrite dialog error: {e}")
                continue

            if (overwrite_dlg.OK is False) or (response is None) or (response[0] == "No"):
                print("❌ User canceled or declined overwrite. Returning to input.")
                continue

        run_task(config, subject_id, subject_group, session_num)

        print("✅ Task complete. Returning to input dialog...")

    
    
    




