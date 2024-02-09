from pywinauto.application import Application
from pywinauto import mouse
import os
import sys
import psutil
import time


# 点赞 操作
def frun_point(dlg, wint, name, tb):
    # 操纵状态
    isclick = False
    for i in dlg.items():
        # 获取评论按钮
        review = i.descendants(control_type='Button', title="评论")
        if review:
            # 评论控件坐标在可点击范围内
            if tb[0] > review[0].rectangle().bottom > tb[1] + 200:
                # 获取点赞的信息
                w = i.descendants(control_type='Edit')
                # 查找点赞信息中有没有name，点过赞，则跳出本次
                if w and str(w).find(name) >= 0:
                    continue
                # 点击评论按钮
                review[0].click_input()
                # 获取赞按钮
                praise = wint.child_window(control_type='Button', title="赞")
                # 点赞
                praise.click_input()
                # 状态为点过赞
                isclick = True
        else:
            isclick = False
        time.sleep(0.1)
    return isclick


# 主循环函数
def fun_main(name, wint):
    vain = 0
    # 中心点、坐标范围
    rect = wint.rectangle()
    cxy = int((rect.left + rect.right) / 2), int((rect.top + rect.bottom) / 2)
    tb = int(rect.bottom), int(rect.top)
    # 主循环
    while True:
        # 信息列表
        dlg = wint.child_window(control_type='List', title="朋友圈")
        # 点赞操作
        isclick = frun_point(dlg, wint, name, tb)
        # 连续5次没有点赞，则结束程序
        if isclick:
            vain = 0
        else:
            vain += 1
            if vain >= 10:
                sys.exit(0)
        # 滚动
        mouse.scroll(coords=cxy, wheel_dist=-3)
        time.sleep(0.1)


# 连接应用，获取应用实例
def fun_app(process_name):
    # 获取后台进程号
    pl = psutil.pids()
    for pid in pl:
        # 进程号对应应用名称
        if psutil.Process(pid).name() == process_name:
            # 获取应用启动路径
            f = os.popen("wmic process where handle=%s get ExecutablePath" % pid, "r")
            path = f.read().replace("ExecutablePath", "").strip()
            f.close()
            # 启动应用，带前台效果
            Application(backend="uia").start(path, timeout=5)
            # 连接应用，获取应用实例
            app = Application(backend='uia').connect(process=pid, timeout=5)
            return app
    print('请启动并登录pc版微信')


# 获取朋友圈窗口
def fun_wint(app):
    # 获取主窗口
    wint = app.window(class_name="WeChatMainWndForPC", title="微信")
    wint.wait('ready', timeout=5, retry_interval=5)
    # 朋友圈按钮
    # dlg = wint.child_window(control_type='Button', title="朋友圈")
    # dlg.click_input()
    return app.window(class_name="SnsWnd", title="朋友圈")


# 获取微信名称
def fun_name(wint):
    a = wint.descendants(control_type='Edit')
    return str(a[0]).split("'")[1]


if __name__ == '__main__':
    for i in ['不要动鼠标',3,2,1]:
        time.sleep(1)
        print(i)
    # 应用名称
    process_name = 'WeChat.exe'
    # 获取应用实例
    app = fun_app(process_name)
    # 获取朋友圈窗口
    wint = fun_wint(app)
    # 获取微信名称
    name = fun_name(wint)
    # 主循环
    fun_main(name, wint)
