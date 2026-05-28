#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼠标自动点击小程序
快捷键：F10 开始/暂停，F12 结束
功能：记录鼠标位置，每隔1-2秒随机偏移点击，偏移量3-5像素
"""

import time
import random
import threading
from pynput import keyboard, mouse
from pynput.mouse import Controller, Button

class AutoClicker:
    def __init__(self):
        self.mouse = Controller()
        self.base_position = None
        self.running = False
        self.paused = False
        self.stop_flag = False
        
    def set_base_position(self):
        self.base_position = self.mouse.position
        print(f"[记录位置] X={self.base_position[0]}, Y={self.base_position[1]}")
        
    def random_click(self):
        if not self.base_position:
            return
        offset_x = random.choice([-1, 1]) * random.randint(3, 5)
        offset_y = random.choice([-1, 1]) * random.randint(3, 5)
        target_x = self.base_position[0] + offset_x
        target_y = self.base_position[1] + offset_y
        self.mouse.position = (target_x, target_y)
        time.sleep(0.05)
        self.mouse.click(Button.left)
        print(f"[点击] X={target_x}, Y={target_y} (偏移: {offset_x:+d}, {offset_y:+d})")
        
    def click_loop(self):
        while not self.stop_flag:
            if self.running and not self.paused and self.base_position:
                self.random_click()
                sleep_time = random.uniform(1.0, 2.0)
                time.sleep(sleep_time)
            else:
                time.sleep(0.1)
                
    def start(self):
        if not self.base_position:
            self.set_base_position()
        if not self.running:
            self.running = True
            self.paused = False
            print("[状态] 开始运行")
        elif self.paused:
            self.paused = False
            print("[状态] 继续运行")
            
    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            print("[状态] 已暂停")
            
    def toggle(self):
        if not self.running or self.paused:
            self.start()
        else:
            self.pause()
            
    def stop(self):
        self.stop_flag = True
        print("[状态] 程序已结束")
        return False

def main():
    print("=" * 50)
    print("鼠标自动点击小程序")
    print("=" * 50)
    print("快捷键说明：")
    print("  F10 - 开始/暂停 (首次按F10记录鼠标位置)")
    print("  F12 - 结束程序")
    print("=" * 50)
    clicker = AutoClicker()
    click_thread = threading.Thread(target=clicker.click_loop, daemon=True)
    click_thread.start()
    def on_press(key):
        try:
            if key == keyboard.Key.f10:
                clicker.start()
            elif key == keyboard.Key.f11:
                clicker.pause()
            elif key == keyboard.Key.f12:
                return clicker.stop()
        except Exception as e:
            print(f"[错误] {e}")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("程序已退出")

if __name__ == "__main__":
    main()
