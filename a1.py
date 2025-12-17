# 猴子吃香蕉做鬼脸动画 - Python tkinter 版本
import tkinter as tk
import math
import random

class MonkeyAnimation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐵 吃香蕉做鬼脸的小猴子 🍌")
        self.root.geometry("500x600")
        self.root.configure(bg="#87CEEB")
        
        self.canvas = tk.Canvas(self.root, width=500, height=550, bg="#87CEEB", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # 动画状态
        self.frame = 0
        self.mouth_open = False
        self.eye_wink = False
        self.tongue_angle = 0
        self.banana_y = 0
        self.bananas_eaten = 0
        
        # 绘制初始场景
        self.draw_scene()
        
        # 标题
        self.label = tk.Label(self.root, text=f"🍌 已吃香蕉: {self.bananas_eaten} 根", 
                             font=("Microsoft YaHei", 14), bg="#87CEEB", fg="#333")
        self.label.pack()
        
        # 开始动画
        self.animate()
        
    def draw_scene(self):
        self.canvas.delete("all")
        
        # 背景装饰 - 草地
        self.canvas.create_rectangle(0, 450, 500, 550, fill="#90EE90", outline="")
        
        # 画太阳
        self.canvas.create_oval(400, 30, 470, 100, fill="#FFD700", outline="#FFA500", width=3)
        
        # 画云朵
        for x in [50, 200, 350]:
            self.draw_cloud(x, 50 + random.randint(-10, 10))
        
        # 画猴子
        self.draw_monkey(250, 280)
        
    def draw_cloud(self, x, y):
        for dx, dy in [(0, 0), (20, -10), (40, 0), (15, 10), (35, 10)]:
            self.canvas.create_oval(x+dx, y+dy, x+dx+30, y+dy+25, fill="white", outline="")
    
    def draw_monkey(self, cx, cy):
        # === 身体 ===
        self.canvas.create_oval(cx-50, cy+40, cx+50, cy+140, fill="#8B4513", outline="#5D3A1A", width=2)
        # 肚子
        self.canvas.create_oval(cx-30, cy+55, cx+30, cy+120, fill="#DEB887", outline="")
        
        # === 腿 ===
        self.canvas.create_oval(cx-40, cy+110, cx-10, cy+170, fill="#8B4513", outline="#5D3A1A", width=2)
        self.canvas.create_oval(cx+10, cy+110, cx+40, cy+170, fill="#8B4513", outline="#5D3A1A", width=2)
        # 脚
        self.canvas.create_oval(cx-50, cy+155, cx-10, cy+180, fill="#8B4513", outline="#5D3A1A", width=2)
        self.canvas.create_oval(cx+10, cy+155, cx+50, cy+180, fill="#8B4513", outline="#5D3A1A", width=2)
        
        # === 尾巴 ===
        tail_wave = math.sin(self.frame * 0.2) * 10
        self.canvas.create_arc(cx+40, cy+60, cx+120, cy+140, start=0, extent=180, 
                              style=tk.ARC, outline="#8B4513", width=8)
        
        # === 手臂 ===
        # 左臂 (拿香蕉)
        arm_angle = math.sin(self.frame * 0.15) * 10
        left_arm_end_x = cx - 80 + arm_angle
        left_arm_end_y = cy - 20 + self.banana_y
        self.canvas.create_line(cx-45, cy+60, left_arm_end_x, left_arm_end_y, 
                               fill="#8B4513", width=20, capstyle=tk.ROUND)
        # 左手
        self.canvas.create_oval(left_arm_end_x-15, left_arm_end_y-15, 
                               left_arm_end_x+15, left_arm_end_y+15, fill="#DEB887", outline="")
        
        # 香蕉
        banana_x = left_arm_end_x + 10
        banana_y = left_arm_end_y - 30
        self.draw_banana(banana_x, banana_y)
        
        # 右臂 (挥手)
        wave = math.sin(self.frame * 0.3) * 30
        self.canvas.create_line(cx+45, cy+60, cx+90, cy+10+wave, 
                               fill="#8B4513", width=20, capstyle=tk.ROUND)
        # 右手
        self.canvas.create_oval(cx+75, cy-5+wave, cx+105, cy+25+wave, fill="#DEB887", outline="")
        
        # === 头 ===
        self.canvas.create_oval(cx-60, cy-80, cx+60, cy+50, fill="#8B4513", outline="#5D3A1A", width=2)
        
        # 耳朵
        self.canvas.create_oval(cx-75, cy-40, cx-45, cy-5, fill="#8B4513", outline="#5D3A1A", width=2)
        self.canvas.create_oval(cx-68, cy-33, cx-52, cy-12, fill="#DEB887", outline="")
        self.canvas.create_oval(cx+45, cy-40, cx+75, cy-5, fill="#8B4513", outline="#5D3A1A", width=2)
        self.canvas.create_oval(cx+52, cy-33, cx+68, cy-12, fill="#DEB887", outline="")
        
        # 脸
        self.canvas.create_oval(cx-40, cy-50, cx+40, cy+30, fill="#DEB887", outline="")
        
        # === 眉毛 (做鬼脸) ===
        brow_y = cy - 45 + math.sin(self.frame * 0.2) * 5
        self.canvas.create_line(cx-30, brow_y, cx-10, brow_y-8, fill="#5D3A1A", width=4, capstyle=tk.ROUND)
        self.canvas.create_line(cx+10, brow_y-8, cx+30, brow_y, fill="#5D3A1A", width=4, capstyle=tk.ROUND)
        
        # === 眼睛 ===
        # 左眼 (眨眼)
        left_eye_height = 3 if self.eye_wink else 20
        self.canvas.create_oval(cx-30, cy-35, cx-10, cy-35+left_eye_height, fill="white", outline="black", width=2)
        if not self.eye_wink:
            pupil_x = cx - 20 + math.sin(self.frame * 0.25) * 5
            pupil_y = cy - 28 + math.cos(self.frame * 0.25) * 3
            self.canvas.create_oval(pupil_x-5, pupil_y-5, pupil_x+5, pupil_y+5, fill="black")
            self.canvas.create_oval(pupil_x-2, pupil_y-3, pupil_x+1, pupil_y, fill="white")
        
        # 右眼
        self.canvas.create_oval(cx+10, cy-35, cx+30, cy-15, fill="white", outline="black", width=2)
        pupil_x = cx + 20 + math.sin(self.frame * 0.25) * 5
        pupil_y = cy - 28 + math.cos(self.frame * 0.25) * 3
        self.canvas.create_oval(pupil_x-5, pupil_y-5, pupil_x+5, pupil_y+5, fill="black")
        self.canvas.create_oval(pupil_x-2, pupil_y-3, pupil_x+1, pupil_y, fill="white")
        
        # === 脸红 ===
        blush_alpha = abs(math.sin(self.frame * 0.1))
        self.canvas.create_oval(cx-45, cy-15, cx-30, cy-5, fill="#FFB6C1", outline="")
        self.canvas.create_oval(cx+30, cy-15, cx+45, cy-5, fill="#FFB6C1", outline="")
        
        # === 鼻子 ===
        self.canvas.create_oval(cx-12, cy-8, cx+12, cy+8, fill="#A0522D", outline="#5D3A1A", width=2)
        self.canvas.create_oval(cx-8, cy-2, cx-3, cy+4, fill="#5D3A1A", outline="")
        self.canvas.create_oval(cx+3, cy-2, cx+8, cy+4, fill="#5D3A1A", outline="")
        
        # === 嘴巴 (吃东西 + 做鬼脸) ===
        mouth_height = 30 if self.mouth_open else 15
        self.canvas.create_oval(cx-20, cy+8, cx+20, cy+8+mouth_height, 
                               fill="#8B0000", outline="#5D3A1A", width=2)
        
        # 牙齿
        if self.mouth_open:
            for i in range(4):
                tx = cx - 12 + i * 8
                self.canvas.create_rectangle(tx, cy+10, tx+6, cy+18, fill="white", outline="")
        
        # 舌头 (做鬼脸)
        tongue_x = cx + math.sin(self.tongue_angle) * 10
        self.canvas.create_oval(tongue_x-12, cy+20, tongue_x+12, cy+50, fill="#FF6B6B", outline="#CC5555", width=2)
        
    def draw_banana(self, x, y):
        # 香蕉主体
        self.canvas.create_arc(x-30, y-10, x+30, y+30, start=0, extent=180,
                              fill="#FFD700", outline="#DAA520", width=2, style=tk.CHORD)
        # 香蕉尖
        self.canvas.create_oval(x+20, y+5, x+35, y+20, fill="#8B4513", outline="")
        # 香蕉柄
        self.canvas.create_rectangle(x-32, y+5, x-25, y+15, fill="#8B4513", outline="")
    
    def animate(self):
        self.frame += 1
        
        # 眨眼逻辑
        if self.frame % 60 == 0:
            self.eye_wink = True
        elif self.frame % 60 == 5:
            self.eye_wink = False
        
        # 嘴巴开合
        if self.frame % 30 < 15:
            self.mouth_open = True
        else:
            self.mouth_open = False
        
        # 舌头摇摆
        self.tongue_angle += 0.3
        
        # 香蕉移动 (吃香蕉动作)
        self.banana_y = math.sin(self.frame * 0.1) * 15
        
        # 每100帧吃一根香蕉
        if self.frame % 100 == 0:
            self.bananas_eaten += 1
            self.label.config(text=f"🍌 已吃香蕉: {self.bananas_eaten} 根")
        
        # 重绘场景
        self.draw_scene()
        
        # 继续动画 (约30fps)
        self.root.after(33, self.animate)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MonkeyAnimation()
    app.run()
