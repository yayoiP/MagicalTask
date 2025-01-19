from pystray import Icon, MenuItem, Menu
from PIL import Image
import time,threading,os,asyncio
from tkinter import messagebox
import threading,TkEasyGUI as sg
import ctypes,json,webbrowser,subprocess
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

datas = json.load(open('data.json', 'r'))
icon=""
menus=[]
async def getdata():
    global datas,icon,menus
    layout=[[sg.Text("name:")],
            [sg.InputText("",key='name')],
            [sg.Text("type:")],
            [sg.Listbox(["web","app"], default_value="web", size=(100, 10), enable_events=True, key='list')],
            [sg.Text("path:")],
            [sg.InputText("",key='path'),sg.FileBrowse(key="file")],
            [sg.Button("作成")]]
    window = sg.Window("new",layout)
    while window.is_alive():
        event, values = window.read()
        if event in (None, '終了'):
            break
        elif event == "file":
            event["path"].update(value["file"])
        elif event == "作成":
            with open("data.json","w") as f:
                if os.path.exists(values['path']) or values["list"]==["web"]:
                    datas.append(
                    {
                        "name":values['name'],
                        "value":values['path'],
                        "protcol":values['list'][0]
                    }
                             )
                    json.dump(datas, f)
                else:
                    json.dump(datas, f)
                    messagebox.showerror("エラー", "正しく")
            break
    window.close()
    menus=[MenuItem(datas[i]["name"] ,startfunc(i)) for i in range(len(datas))]
    icon.update_menu()

class taskTray:
    def __init__(self, image):
        self.status = False
        global icon,menus
        menus=[MenuItem(datas[i]["name"] ,startfunc(i)) for i in range(len(datas))]
        ## アイコンの画像
        image = Image.open(image)
        ## 右クリックで表示されるメニュー
        menu = Menu(
                    lambda: (i for i in self.getmenu())
                )


        icon = Icon(name='nameTray', title='titleTray', icon=image, menu=menu)

    def getmenu(self):
        global menus
        aaa=[MenuItem('+new', self.doTask),
                    MenuItem('Exit', self.stopProgram)]
        return aaa+menus
    
    def doTask(self):
        asyncio.run(getdata())
        
    def stopProgram(self):
        global icon
        self.status = False

        ## 停止
        icon.stop()

    def runProgram(self):
        self.status = True
        global icon

        ## スケジュールの実行
        task_thread = threading.Thread(target=self.runSchedule)
        task_thread.start()

        ## 実行
        icon.run()
if True:
    def startfunc(number):
        try:
            def runfunc():
                global datas
                data=datas[number]
                if data["protcol"]=="web":
                    webbrowser.open(data["value"])
                elif data["protcol"]=="app":
                    subprocess.Popen([data["value"]])
                    print(data)
            return runfunc
        except:
            messagebox.showerror("エラー", "何らかのエラーが発生")

if __name__ == '__main__':
    system_tray = taskTray(image="icon.jpg")
    icon.run()
