# 玄机命理 - 神秘命理软件
# 包含：算命大师、黄道吉日、老黄历、婚姻配对、今日禁忌

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta
import calendar

class MysteryFortuneApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✨ 玄机命理 - 洞悉天机 ✨")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0a0a1a")
        self.root.resizable(False, False)
        
        # 神秘配色方案（亮丽清晰版）
        self.colors = {
            'bg_dark': '#0a0a1a',
            'bg_card': '#1a1a2e',
            'bg_hover': '#2a2a4a',
            'gold': '#ffea00',           # 更亮的金色
            'gold_dark': '#ffc107',       # 亮橙金色
            'purple': '#a855f7',          # 明亮紫色
            'purple_light': '#d8b4fe',    # 浅紫色
            'red': '#ff5555',             # 鲜红色
            'green': '#22c55e',           # 鲜绿色
            'text': '#ffffff',            # 纯白色文字
            'text_dim': '#a0a0a0',        # 灰色文字提亮
            'cyan': '#00d4ff',            # 青色
            'orange': '#ff9500'           # 橙色
        }
        
        # 天干地支数据
        self.tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        self.shengxiao = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        self.wuxing = ['金', '木', '水', '火', '土']
        
        # 农历月份和日期
        self.lunar_months = ['正月', '二月', '三月', '四月', '五月', '六月', 
                            '七月', '八月', '九月', '十月', '冬月', '腊月']
        self.lunar_days = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                          '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                          '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
        
        self.current_panel = None
        self.setup_ui()
        
    def setup_ui(self):
        # 顶部标题栏
        self.create_header()
        
        # 主内容区
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧导航菜单
        self.create_nav_menu()
        
        # 右侧内容区
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['bg_card'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 默认显示首页
        self.show_home()
        
    def create_header(self):
        # 第一排空白或极简
        header = tk.Frame(self.root, bg=self.colors['bg_dark'], height=10)
        header.pack(fill=tk.X, padx=20, pady=(10, 0))
        
    def create_info_bar(self):
        # 第二排左侧标题
        info_bar = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        info_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # 左侧副标题
        subtitle = tk.Label(info_bar, text="✨ 洞悉天机 · 趋吉避凶 ✨", 
                           font=("Microsoft YaHei", 14, "bold"),
                           fg=self.colors['gold'], bg=self.colors['bg_card'])
        subtitle.pack(side=tk.LEFT, padx=10)
        
    def create_nav_menu(self):
        nav_frame = tk.Frame(self.main_frame, bg=self.colors['bg_card'], width=180)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y)
        nav_frame.pack_propagate(False)
        
        menu_items = [
            ("🏠", "首    页", self.show_home),
            ("🔮", "算命大师", self.show_fortune_master),
            ("📅", "黄道吉日", self.show_auspicious_days),
            ("📜", "老 黄 历", self.show_almanac),
            ("💑", "婚姻配对", self.show_marriage_match),
            ("⚠", "今日禁忌", self.show_taboos),
        ]
        
        self.nav_buttons = []
        for icon, text, command in menu_items:
            btn_frame = tk.Frame(nav_frame, bg=self.colors['bg_card'])
            btn_frame.pack(fill=tk.X, pady=2)
            
            btn = tk.Label(btn_frame, text=f" {icon}  {text}", 
                          font=("Microsoft YaHei", 13),
                          fg=self.colors['text'], bg=self.colors['bg_card'],
                          anchor="w", padx=15, pady=12, cursor="hand2")
            btn.pack(fill=tk.X)
            
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['bg_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors['bg_card']))
            btn.bind("<Button-1>", lambda e, cmd=command, b=btn: self.on_nav_click(cmd, b))
            
            self.nav_buttons.append(btn)
    
    def on_nav_click(self, command, btn):
        for b in self.nav_buttons:
            b.configure(bg=self.colors['bg_card'], fg=self.colors['text'])
        btn.configure(bg=self.colors['purple'], fg=self.colors['gold'])
        command()
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # 每次清除后重新添加信息栏
        self.create_info_bar()
            
    def create_panel_title(self, icon, title, subtitle=""):
        title_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        tk.Label(title_frame, text=f"{icon} {title}", 
                font=("Microsoft YaHei", 20, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_card']).pack(anchor="w")
        
        # 副标题行（左侧副标题 + 右侧日期）
        sub_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        sub_frame.pack(fill=tk.X, padx=20, pady=(5, 8))
        
        if subtitle:
            tk.Label(sub_frame, text=subtitle, 
                    font=("Microsoft YaHei", 11),
                    fg=self.colors['text_dim'], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        # 右侧日期信息（与副标题平行对齐）
        today = datetime.now()
        date_str = today.strftime("%Y年%m月%d日")
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        lunar_info = self.get_lunar_date(today)
        
        tk.Label(sub_frame, text=f"📅 {date_str} {weekdays[today.weekday()]}  │  🌙 {lunar_info}", 
                font=("Microsoft YaHei", 11),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.RIGHT)
        
        # 分隔线
        separator = tk.Frame(self.content_frame, bg=self.colors['gold_dark'], height=2)
        separator.pack(fill=tk.X, padx=20)
        
    def show_home(self):
        self.clear_content()
        self.create_panel_title("🏠", "欢迎使用玄机命理", "探索命运奥秘，把握人生方向")
        
        # 功能卡片区
        cards_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        features = [
            ("🔮", "算命大师", "八字命理、紫微斗数\n生辰解析、运势预测", self.colors['purple']),
            ("📅", "黄道吉日", "择日择时、婚嫁吉日\n开业搬家、出行良辰", self.colors['green']),
            ("📜", "老 黄 历", "每日宜忌、农历信息\n节气物候、传统文化", self.colors['gold_dark']),
            ("💑", "婚姻配对", "生肖配对、八字合婚\n姻缘分析、幸福指数", self.colors['red']),
            ("⚠", "今日禁忌", "每日冲煞、忌讳事项\n趋吉避凶、平安顺遂", "#e67e22"),
        ]
        
        for i, (icon, title, desc, color) in enumerate(features):
            row, col = divmod(i, 3)
            card = tk.Frame(cards_frame, bg=self.colors['bg_hover'], padx=15, pady=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            tk.Label(card, text=icon, font=("Arial", 32), 
                    fg=color, bg=self.colors['bg_hover']).pack()
            tk.Label(card, text=title, font=("Microsoft YaHei", 14, "bold"),
                    fg=self.colors['text'], bg=self.colors['bg_hover']).pack(pady=(5,0))
            tk.Label(card, text=desc, font=("Microsoft YaHei", 10),
                    fg=self.colors['text_dim'], bg=self.colors['bg_hover'],
                    justify=tk.CENTER).pack(pady=(5,0))
        
        for i in range(3):
            cards_frame.columnconfigure(i, weight=1)
    
    def show_fortune_master(self):
        self.clear_content()
        self.create_panel_title("🔮", "算命大师", "输入生辰八字，揭示命运密码")
        
        # 输入区域
        input_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # 生日输入
        tk.Label(input_frame, text="请选择出生日期：", font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).grid(row=0, column=0, sticky="w", pady=5)
        
        date_frame = tk.Frame(input_frame, bg=self.colors['bg_card'])
        date_frame.grid(row=0, column=1, padx=10)
        
        self.year_var = tk.StringVar(value="1990")
        self.month_var = tk.StringVar(value="1")
        self.day_var = tk.StringVar(value="1")
        self.hour_var = tk.StringVar(value="12")
        
        years = [str(y) for y in range(1940, 2025)]
        ttk.Combobox(date_frame, textvariable=self.year_var, values=years, width=6).pack(side=tk.LEFT)
        tk.Label(date_frame, text="年", fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=2)
        
        ttk.Combobox(date_frame, textvariable=self.month_var, values=[str(m) for m in range(1,13)], width=4).pack(side=tk.LEFT)
        tk.Label(date_frame, text="月", fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=2)
        
        ttk.Combobox(date_frame, textvariable=self.day_var, values=[str(d) for d in range(1,32)], width=4).pack(side=tk.LEFT)
        tk.Label(date_frame, text="日", fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=2)
        
        ttk.Combobox(date_frame, textvariable=self.hour_var, values=[str(h) for h in range(0,24)], width=4).pack(side=tk.LEFT)
        tk.Label(date_frame, text="时", fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=2)
        
        # 测算按钮
        calc_btn = tk.Button(input_frame, text="🔮 开始测算", font=("Microsoft YaHei", 12, "bold"),
                            bg=self.colors['purple'], fg="white", padx=20, pady=8,
                            cursor="hand2", command=self.calculate_fortune)
        calc_btn.grid(row=0, column=2, padx=20)
        
        # 结果区域
        self.fortune_result = tk.Frame(self.content_frame, bg=self.colors['bg_hover'])
        self.fortune_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
    def calculate_fortune(self):
        for widget in self.fortune_result.winfo_children():
            widget.destroy()
            
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        day = int(self.day_var.get())
        hour = int(self.hour_var.get())
        
        # 计算八字
        year_gan = self.tiangan[(year - 4) % 10]
        year_zhi = self.dizhi[(year - 4) % 12]
        shengxiao = self.shengxiao[(year - 4) % 12]
        
        month_gan = self.tiangan[(year * 12 + month + 3) % 10]
        month_zhi = self.dizhi[(month + 1) % 12]
        
        day_gan = self.tiangan[(year * 365 + month * 30 + day) % 10]
        day_zhi = self.dizhi[(year * 365 + month * 30 + day) % 12]
        
        hour_zhi_idx = (hour + 1) // 2 % 12
        hour_gan = self.tiangan[(int(self.tiangan.index(day_gan)) * 2 + hour_zhi_idx) % 10]
        hour_zhi = self.dizhi[hour_zhi_idx]
        
        bazi = f"{year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}"
        
        # 五行映射
        wuxing_map = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
        zhi_wuxing = {'子':'水','丑':'土','寅':'木','卯':'木','辰':'土','巳':'火','午':'火','未':'土','申':'金','酉':'金','戌':'土','亥':'水'}
        
        # 统计五行
        all_elements = [year_gan, month_gan, day_gan, hour_gan, year_zhi, month_zhi, day_zhi, hour_zhi]
        wuxing_count = {'金':0, '木':0, '水':0, '火':0, '土':0}
        for e in all_elements[:4]:
            wuxing_count[wuxing_map[e]] += 1
        for e in all_elements[4:]:
            wuxing_count[zhi_wuxing[e]] += 1
        
        day_wuxing = wuxing_map[day_gan]  # 日主五行
        
        # 五行生克关系
        sheng_map = {'木':'火', '火':'土', '土':'金', '金':'水', '水':'木'}
        ke_map = {'木':'土', '土':'水', '水':'火', '火':'金', '金':'木'}
        sheng_wo = [k for k,v in sheng_map.items() if v == day_wuxing][0]  # 生我者
        wo_sheng = sheng_map[day_wuxing]  # 我生者
        ke_wo = [k for k,v in ke_map.items() if v == day_wuxing][0]  # 克我者
        wo_ke = ke_map[day_wuxing]  # 我克者
        
        # 日主强弱判断
        help_count = wuxing_count[day_wuxing] + wuxing_count[sheng_wo]
        drain_count = wuxing_count[wo_sheng] + wuxing_count[wo_ke] + wuxing_count[ke_wo]
        is_strong = help_count >= drain_count
        
        # 喜用神分析
        if is_strong:
            xi_shen = [wo_sheng, wo_ke, ke_wo]
            ji_shen = [day_wuxing, sheng_wo]
        else:
            xi_shen = [day_wuxing, sheng_wo]
            ji_shen = [wo_sheng, wo_ke, ke_wo]
        
        # 十神分析
        shishen_map = {
            ('同','同'): '比肩', ('同','异'): '劫财',
            ('生','同'): '枭印', ('生','异'): '正印',
            ('泄','同'): '食神', ('泄','异'): '伤官',
            ('克','同'): '偏财', ('克','异'): '正财',
            ('被克','同'): '七杀', ('被克','异'): '正官'
        }
        
        # 格局判断
        geju_list = ["正印格", "偏印格", "食神格", "伤官格", "正财格", "偏财格", 
                    "正官格", "七杀格", "建禄格", "羊刃格"]
        geju = random.choice(geju_list)
        
        # 创建可滚动区域
        canvas = tk.Canvas(self.fortune_result, bg=self.colors['bg_hover'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.fortune_result, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg_hover'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=720)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # 标题
        tk.Label(scroll_frame, text="📿 命理分析报告", 
                font=("Microsoft YaHei", 16, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(pady=15)
        
        # === 基本信息卡片 ===
        info_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        info_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # 标题 + 四柱同行
        header_row = tk.Frame(info_frame, bg=self.colors['bg_card'])
        header_row.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(header_row, text="① 八字命盘", font=("Microsoft YaHei", 12, "bold"),
                fg=self.colors['cyan'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=5)
        
        pillars = [("年", year_gan, year_zhi), ("月", month_gan, month_zhi), 
                  ("日", day_gan, day_zhi), ("时", hour_gan, hour_zhi)]
        for name, gan, zhi in pillars:
            col_frame = tk.Frame(header_row, bg=self.colors['bg_hover'], padx=8, pady=3)
            col_frame.pack(side=tk.LEFT, padx=3)
            tk.Label(col_frame, text=f"{name}:{gan}{zhi}", font=("Microsoft YaHei", 11, "bold"),
                    fg=self.colors['gold'], bg=self.colors['bg_hover']).pack()
        
        # 生肖/日主/格局 同行
        tk.Label(header_row, text=f"  🐲{shengxiao}  日主:{day_gan}{day_wuxing}  {geju}", 
                font=("Microsoft YaHei", 10),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=10)
        
        # === 五行分析 ===
        wx_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        wx_frame.pack(fill=tk.X, padx=15, pady=5)
        
        wx_row = tk.Frame(wx_frame, bg=self.colors['bg_card'])
        wx_row.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(wx_row, text="② 五行", font=("Microsoft YaHei", 12, "bold"),
                fg=self.colors['cyan'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=5)
        
        wuxing_colors = {'金':'#E8E8E8', '木':'#22c55e', '水':'#00d4ff', '火':'#ff5555', '土':'#ffc107'}
        for wx, count in wuxing_count.items():
            status = "旺" if count >= 3 else "平" if count >= 1 else "弱"
            tk.Label(wx_row, text=f"{wx}:{count}{status}", font=("Microsoft YaHei", 10, "bold"),
                    fg=wuxing_colors[wx], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=4)
        
        # 日主强弱
        strength = "身旺" if is_strong else "身弱"
        strength_color = self.colors['green'] if is_strong else self.colors['orange']
        tk.Label(wx_row, text=f"  日主:{strength}", font=("Microsoft YaHei", 10, "bold"),
                fg=strength_color, bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=8)
        
        # === 喜忌分析 ===
        xiji_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        xiji_frame.pack(fill=tk.X, padx=15, pady=8)
        
        tk.Label(xiji_frame, text="③ 喜用神与忌神", font=("Microsoft YaHei", 13, "bold"),
                fg=self.colors['cyan'], bg=self.colors['bg_card']).pack(anchor="w", padx=15, pady=8)
        
        xiji_row = tk.Frame(xiji_frame, bg=self.colors['bg_card'])
        xiji_row.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(xiji_row, text="✅ 喜用神：", font=("Microsoft YaHei", 11),
                fg=self.colors['green'], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        for xs in xi_shen[:2]:
            tk.Label(xiji_row, text=f" {xs} ", font=("Microsoft YaHei", 11, "bold"),
                    fg=wuxing_colors[xs], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        tk.Label(xiji_row, text="    ❌ 忌神：", font=("Microsoft YaHei", 11),
                fg=self.colors['red'], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        for js in ji_shen[:2]:
            tk.Label(xiji_row, text=f" {js} ", font=("Microsoft YaHei", 11, "bold"),
                    fg=wuxing_colors[js], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        # === 命理解读 ===
        jiedu_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        jiedu_frame.pack(fill=tk.X, padx=15, pady=8)
        
        tk.Label(jiedu_frame, text="④ 命理综合解读", font=("Microsoft YaHei", 13, "bold"),
                fg=self.colors['cyan'], bg=self.colors['bg_card']).pack(anchor="w", padx=15, pady=8)
        
        # 根据日主五行和强弱生成解读
        readings = {
            '木': {
                True: ["日主甲木身旺，如参天大树，刚正不阿，领导力强，适合创业或管理岗位。",
                       "木旺喜金来雕琢，方能成器，宜从事纪律性强的工作。",
                       "财运方面，中年后财库渐丰，有積蓄之象。"],
                False: ["日主甲木身弱，如幼苗无依，需得水木生扶，方能茂盛。",
                       "适合团队合作，借助贵人之力发展事业。",
                       "心态平和，不争不抢，婚姻缘分来得较晚，但质量高。"]},
            '火': {
                True: ["日主丙火身旺，如日中天，光明磊落，热情开朗，有领袖气质。",
                       "火旺则燥，需水来济，否则性格急躁，宜修身养性。",
                       "事业运佳，年轻时即有成就，中年可达高峰。"],
                False: ["日主丙火身弱，如火烛微弱，需木来生扶，方能光耀。",
                       "性格温和，善于交际，人缘极佳，适合公关、销售类工作。",
                       "财运平稳，不宜冒险投资，稳健经营为佳。"]},
            '土': {
                True: ["日主戊土身旺，如山岳稳重，诚实守信，有担当，但固执。",
                       "土旺喜木来疏，否则过于保守，错失良机。",
                       "适合稳定的工作环境，如政府、国企、教育等行业。"],
                False: ["日主戊土身弱，如田园乏水，需火土生扶，方能肥沃。",
                       "性格随和，包容性强，人缘好，但需增强自信。",
                       "中年后运势渐入佳境，大器晚成。"]},
            '金': {
                True: ["日主庚金身旺，如刃剑出鞘，果断刚毅，但需火来练，方成利器。",
                       "金旺克木太过，宜注意人际关系，避免过于强势。",
                       "武职、法律、金融行业发展佳，有正财运。"],
                False: ["日主庚金身弱，如饰品小巧，需土金生扶，方显价值。",
                       "心思细密，善于策划，适合幕后工作或技术岗位。",
                       "财运需耐心经营，不可急于求成，稳中求进。"]},
            '水': {
                True: ["日主壬水身旺，如江河汹涌，智慧过人，变通能力强。",
                       "水旺则泪，需土来制，否则思绪不定，难以专注。",
                       "适合智力工作如研究、写作、咨询等，有海外发展运。"],
                False: ["日主壬水身弱，如源头细流，需金水生扶，方能汇流成河。",
                       "性格温顺，适应力强，人缘好，婚姻和美。",
                       "财运需贵人提携，合作经营为佳，不宜单打独斗。"]}
        }
        
        my_readings = readings.get(day_wuxing, readings['木'])[is_strong]
        
        for reading in my_readings:
            tk.Label(jiedu_frame, text=f"  ● {reading}", font=("Microsoft YaHei", 11),
                    fg=self.colors['text'], bg=self.colors['bg_card'],
                    wraplength=650, justify=tk.LEFT).pack(anchor="w", padx=15, pady=4)
        
        # === 流年运势 ===
        yunshi_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        yunshi_frame.pack(fill=tk.X, padx=15, pady=8)
        
        tk.Label(yunshi_frame, text="⑤ 流年运势分析", font=("Microsoft YaHei", 13, "bold"),
                fg=self.colors['cyan'], bg=self.colors['bg_card']).pack(anchor="w", padx=15, pady=8)
        
        current_year = datetime.now().year
        year_gz = f"{self.tiangan[(current_year-4)%10]}{self.dizhi[(current_year-4)%12]}年"
        year_wx = wuxing_map[self.tiangan[(current_year-4)%10]]
        
        if year_wx in xi_shen:
            year_luck = "大吉"
            luck_color = self.colors['gold']
            year_desc = "流年为喜用神，诸事顺遍，可積极进取。"
        elif year_wx == day_wuxing:
            year_luck = "平稳"
            luck_color = self.colors['green']
            year_desc = "流年与日主同元，运势平稳，宜守不宜攻。"
        else:
            year_luck = "平常"
            luck_color = self.colors['orange']
            year_desc = "流年与命局有冲，宜谨慎行事，避免重大决策。"
        
        tk.Label(yunshi_frame, text=f"📅 {year_gz}（{year_wx}）：{year_luck}", 
                font=("Microsoft YaHei", 12, "bold"),
                fg=luck_color, bg=self.colors['bg_card']).pack(anchor="w", padx=15, pady=3)
        tk.Label(yunshi_frame, text=f"  {year_desc}", font=("Microsoft YaHei", 11),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(anchor="w", padx=15, pady=3)
        
        # 结束语
        tk.Label(scroll_frame, text="✨ 命由天定，运由己造，以上仅供参考 ✨", 
                font=("Microsoft YaHei", 11, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(pady=20)

    def show_auspicious_days(self):
        self.clear_content()
        self.create_panel_title("📅", "黄道吉日", "择取良辰吉日，顺应天时地利")
        
        # 事项选择
        select_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        select_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(select_frame, text="选择事项类型：", font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        self.event_var = tk.StringVar(value="结婚嫁娶")
        events = ["结婚嫁娶", "搬家入宅", "开业开张", "出行远行", "签约交易", "动土建房"]
        event_combo = ttk.Combobox(select_frame, textvariable=self.event_var, values=events, width=15)
        event_combo.pack(side=tk.LEFT, padx=10)
        
        search_btn = tk.Button(select_frame, text="🔍 查询吉日", font=("Microsoft YaHei", 11),
                              bg=self.colors['green'], fg="white", padx=15,
                              cursor="hand2", command=self.search_auspicious)
        search_btn.pack(side=tk.LEFT, padx=10)
        
        # 结果区
        self.auspicious_result = tk.Frame(self.content_frame, bg=self.colors['bg_hover'])
        self.auspicious_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.search_auspicious()
        
    def search_auspicious(self):
        for widget in self.auspicious_result.winfo_children():
            widget.destroy()
            
        event = self.event_var.get()
        today = datetime.now()
        
        tk.Label(self.auspicious_result, text=f"📅 近三个月「{event}」吉日", 
                font=("Microsoft YaHei", 14, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(pady=10)
        
        # 创建可滚动区域
        canvas = tk.Canvas(self.auspicious_result, bg=self.colors['bg_hover'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.auspicious_result, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg_hover'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 生成12个吉日（三个月内）
        for i in range(12):
            days_add = random.randint(3 + i*7, 10 + i*7)  # 范围扩展到90天
            if days_add > 90:
                days_add = random.randint(80, 90)
            lucky_date = today + timedelta(days=days_add)
            
            day_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
            day_frame.pack(fill=tk.X, padx=10, pady=4)
            
            weekdays = ['一', '二', '三', '四', '五', '六', '日']
            date_str = lucky_date.strftime(f"%Y年%m月%d日 周{weekdays[lucky_date.weekday()]}")
            
            lunar = self.get_lunar_date(lucky_date)
            
            luck_level = random.choice(["★★★★★ 大吉", "★★★★☆ 上吉", "★★★☆☆ 中吉"])
            luck_color = self.colors['gold'] if "大吉" in luck_level else self.colors['green']
            
            tk.Label(day_frame, text=f"📆 {date_str}", font=("Microsoft YaHei", 11, "bold"),
                    fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=15, pady=8)
            tk.Label(day_frame, text=f"({lunar})", font=("Microsoft YaHei", 10),
                    fg=self.colors['purple_light'], bg=self.colors['bg_card']).pack(side=tk.LEFT)
            tk.Label(day_frame, text=luck_level, font=("Microsoft YaHei", 10, "bold"),
                    fg=luck_color, bg=self.colors['bg_card']).pack(side=tk.RIGHT, padx=15)
        
        # 鼠标滚轮支持
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def show_almanac(self):
        self.clear_content()
        self.create_panel_title("📜", "老黄历", "传承千年智慧，指引日常生活")
        
        today = datetime.now()
        
        # 今日信息卡
        info_card = tk.Frame(self.content_frame, bg=self.colors['bg_hover'])
        info_card.pack(fill=tk.X, padx=20, pady=15)
        
        # 日期大字
        date_frame = tk.Frame(info_card, bg=self.colors['bg_hover'])
        date_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(date_frame, text=str(today.day), font=("Arial", 72, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(side=tk.LEFT)
        
        right_info = tk.Frame(date_frame, bg=self.colors['bg_hover'])
        right_info.pack(side=tk.LEFT, padx=20)
        
        tk.Label(right_info, text=today.strftime("%Y年%m月"), font=("Microsoft YaHei", 16),
                fg=self.colors['text'], bg=self.colors['bg_hover']).pack(anchor="w")
        
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        tk.Label(right_info, text=weekdays[today.weekday()], font=("Microsoft YaHei", 14),
                fg=self.colors['text_dim'], bg=self.colors['bg_hover']).pack(anchor="w")
        
        lunar = self.get_lunar_date(today)
        tk.Label(right_info, text=f"农历 {lunar}", font=("Microsoft YaHei", 13),
                fg=self.colors['purple_light'], bg=self.colors['bg_hover']).pack(anchor="w")
        
        # 干支纪年
        year_gz = f"{self.tiangan[(today.year-4)%10]}{self.dizhi[(today.year-4)%12]}年"
        shengxiao = self.shengxiao[(today.year-4)%12]
        tk.Label(right_info, text=f"{year_gz} 【{shengxiao}年】", font=("Microsoft YaHei", 12),
                fg=self.colors['gold_dark'], bg=self.colors['bg_hover']).pack(anchor="w")
        
        # 宜忌信息
        yiji_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        yiji_frame.pack(fill=tk.X, padx=20, pady=10)
        
        yi_list = random.sample(["嫁娶", "祭祀", "出行", "开市", "纳财", "动土", "安床", "入宅", "开光", "修造"], 5)
        ji_list = random.sample(["诉讼", "安葬", "破土", "伐木", "作灶", "掘井", "栽种"], 4)
        
        # 宜
        yi_frame = tk.Frame(yiji_frame, bg=self.colors['bg_card'])
        yi_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(yi_frame, text="  宜  ", font=("Microsoft YaHei", 14, "bold"),
                fg="white", bg=self.colors['green']).pack(side=tk.LEFT, padx=15)
        tk.Label(yi_frame, text="  ".join(yi_list), font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=10)
        
        # 忌
        ji_frame = tk.Frame(yiji_frame, bg=self.colors['bg_card'])
        ji_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(ji_frame, text="  忌  ", font=("Microsoft YaHei", 14, "bold"),
                fg="white", bg=self.colors['red']).pack(side=tk.LEFT, padx=15)
        tk.Label(ji_frame, text="  ".join(ji_list), font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=10)
        
        # 其他信息
        extra_frame = tk.Frame(self.content_frame, bg=self.colors['bg_hover'])
        extra_frame.pack(fill=tk.X, padx=20, pady=10)
        
        extras = [
            ("冲煞", f"冲{random.choice(self.shengxiao)} 煞{random.choice(['东','西','南','北'])}"),
            ("吉神", random.choice(["天德", "月德", "天恩", "福星", "天喜"])),
            ("凶神", random.choice(["五鬼", "死气", "白虎", "天刑", "朱雀"])),
            ("胎神", random.choice(["仓库门外正南", "厨灶碓外东南", "房床栖外正西"])),
        ]
        
        for label, value in extras:
            tk.Label(extra_frame, text=f"{label}：{value}", font=("Microsoft YaHei", 11),
                    fg=self.colors['text'], bg=self.colors['bg_hover']).pack(side=tk.LEFT, padx=20, pady=15)
    
    def show_marriage_match(self):
        self.clear_content()
        self.create_panel_title("💑", "婚姻配对", "测算姻缘契合，共筑幸福家庭")
        
        # 输入区
        input_frame = tk.Frame(self.content_frame, bg=self.colors['bg_card'])
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # 男方
        male_frame = tk.Frame(input_frame, bg=self.colors['bg_card'])
        male_frame.pack(side=tk.LEFT, padx=30)
        
        tk.Label(male_frame, text="👨 男方生肖", font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack()
        self.male_var = tk.StringVar(value="龙")
        ttk.Combobox(male_frame, textvariable=self.male_var, values=self.shengxiao, width=8).pack(pady=5)
        
        # 女方
        female_frame = tk.Frame(input_frame, bg=self.colors['bg_card'])
        female_frame.pack(side=tk.LEFT, padx=30)
        
        tk.Label(female_frame, text="👩 女方生肖", font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_card']).pack()
        self.female_var = tk.StringVar(value="兔")
        ttk.Combobox(female_frame, textvariable=self.female_var, values=self.shengxiao, width=8).pack(pady=5)
        
        # 配对按钮
        match_btn = tk.Button(input_frame, text="💕 开始配对", font=("Microsoft YaHei", 12, "bold"),
                             bg=self.colors['red'], fg="white", padx=20, pady=5,
                             cursor="hand2", command=self.calculate_match)
        match_btn.pack(side=tk.LEFT, padx=30)
        
        # 结果区
        self.match_result = tk.Frame(self.content_frame, bg=self.colors['bg_hover'])
        self.match_result.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
    def calculate_match(self):
        for widget in self.match_result.winfo_children():
            widget.destroy()
            
        male = self.male_var.get()
        female = self.female_var.get()
        
        # 配对结果
        score = random.randint(60, 99)
        
        if score >= 90:
            level = "天作之合"
            color = self.colors['gold']
            desc = "此乃天赐良缘，二人八字相合，五行互补，婚后必定琴瑟和鸣，白头偕老。"
        elif score >= 80:
            level = "上等婚配"
            color = self.colors['green']
            desc = "二人姻缘不浅，性格互补，相处融洽，携手同行定能共创美好未来。"
        elif score >= 70:
            level = "中等婚配"
            color = self.colors['purple_light']
            desc = "姻缘尚可，需要双方多加包容理解，用心经营方能幸福美满。"
        else:
            level = "需要磨合"
            color = "#e67e22"
            desc = "二人性格有所冲突，需要更多沟通与理解，建议婚前多加考虑。"
        
        # 显示结果
        tk.Label(self.match_result, text=f"💑 {male} ❤ {female}", 
                font=("Microsoft YaHei", 18, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(pady=20)
        
        # 契合度圆环效果
        score_frame = tk.Frame(self.match_result, bg=self.colors['bg_hover'])
        score_frame.pack(pady=10)
        
        tk.Label(score_frame, text=f"{score}", font=("Arial", 56, "bold"),
                fg=color, bg=self.colors['bg_hover']).pack()
        tk.Label(score_frame, text="契合指数", font=("Microsoft YaHei", 12),
                fg=self.colors['text_dim'], bg=self.colors['bg_hover']).pack()
        
        tk.Label(self.match_result, text=level, font=("Microsoft YaHei", 20, "bold"),
                fg=color, bg=self.colors['bg_hover']).pack(pady=10)
        
        tk.Label(self.match_result, text=desc, font=("Microsoft YaHei", 12),
                fg=self.colors['text'], bg=self.colors['bg_hover'],
                wraplength=500).pack(pady=10)
        
        # 详细分析
        details = [
            ("性格相合度", random.randint(70, 95)),
            ("价值观契合", random.randint(65, 90)),
            ("生活习惯", random.randint(60, 95)),
            ("财运互补", random.randint(70, 90)),
        ]
        
        detail_frame = tk.Frame(self.match_result, bg=self.colors['bg_card'])
        detail_frame.pack(fill=tk.X, padx=40, pady=20)
        
        for i, (name, val) in enumerate(details):
            tk.Label(detail_frame, text=name, font=("Microsoft YaHei", 11),
                    fg=self.colors['text'], bg=self.colors['bg_card']).grid(row=i, column=0, sticky="w", padx=15, pady=5)
            
            bar_bg = tk.Frame(detail_frame, bg=self.colors['bg_hover'], width=200, height=15)
            bar_bg.grid(row=i, column=1, padx=10, pady=5)
            bar_bg.pack_propagate(False)
            
            bar_fg = tk.Frame(bar_bg, bg=self.colors['purple'], width=val*2, height=15)
            bar_fg.pack(side=tk.LEFT)
            
            tk.Label(detail_frame, text=f"{val}%", font=("Microsoft YaHei", 10, "bold"),
                    fg=self.colors['gold'], bg=self.colors['bg_card']).grid(row=i, column=2, padx=10)
    
    def show_taboos(self):
        self.clear_content()
        self.create_panel_title("⚠", "今日禁忌", "趋吉避凶，平安顺遂")
        
        today = datetime.now()
        
        # 创建可滚动区域
        canvas = tk.Canvas(self.content_frame, bg=self.colors['bg_hover'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg_hover'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=750)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 鼠标滚轮支持
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # 冲煞信息
        chong_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        chong_frame.pack(fill=tk.X, padx=10, pady=10)
        
        chong_shengxiao = random.choice(self.shengxiao)
        sha_direction = random.choice(['东', '西', '南', '北'])
        
        chong_info = tk.Frame(chong_frame, bg=self.colors['bg_card'])
        chong_info.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(chong_info, text=f"⚡ 今日冲 {chong_shengxiao}", font=("Microsoft YaHei", 16, "bold"),
                fg=self.colors['red'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=10)
        tk.Label(chong_info, text=f"🧭 煞 {sha_direction}", font=("Microsoft YaHei", 16, "bold"),
                fg="#e67e22", bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=20)
        
        tk.Label(chong_frame, text=f"属{chong_shengxiao}者今日宜静不宜动，避免往{sha_direction}方向", 
                font=("Microsoft YaHei", 11),
                fg=self.colors['text_dim'], bg=self.colors['bg_card']).pack(anchor="w", padx=25, pady=(0, 10))
        
        # 禁忌事项标题
        tk.Label(scroll_frame, text="🚫 今日禁忌事项", font=("Microsoft YaHei", 14, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(anchor="w", padx=15, pady=(15, 10))
        
        taboos = [
            ("❌ 忌嫁娶", "今日不宜举办婚嫁之事，恐有不顺"),
            ("❌ 忌安葬", "不宜办理丧葬事宜，择日再行"),
            ("❌ 忌动土", "不宜破土动工，恐惊动土神"),
            ("❌ 忌开市", "不宜开张营业，财运不济"),
            ("❌ 忌远行", "不宜出远门，途中多有阻碍"),
        ]
        
        selected_taboos = random.sample(taboos, random.randint(3, 5))
        
        for title, desc in selected_taboos:
            item_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
            item_frame.pack(fill=tk.X, padx=10, pady=4)
            
            tk.Label(item_frame, text=title, font=("Microsoft YaHei", 12, "bold"),
                    fg=self.colors['red'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=15, pady=8)
            tk.Label(item_frame, text=desc, font=("Microsoft YaHei", 11),
                    fg=self.colors['text'], bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=10)
        
        # 化解建议标题
        tk.Label(scroll_frame, text="💡 化解建议", font=("Microsoft YaHei", 14, "bold"),
                fg=self.colors['green'], bg=self.colors['bg_hover']).pack(anchor="w", padx=15, pady=(20, 10))
        
        # 化解建议内容卡片
        tips_frame = tk.Frame(scroll_frame, bg=self.colors['bg_card'])
        tips_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tips = [
            "📿 佩戴本命佛或护身符可化解部分不利",
            "🙏 心存善念，多行善事可积福消灾",
            "❤️ 避免与人争执，和气生财",
            "📅 重要决定可择吉日再行",
            "🎴 家中可摆放平安符或福字辟邪",
            "🌿 多亲近自然，调节身心状态",
        ]
        
        for tip in tips:
            tk.Label(tips_frame, text=tip, font=("Microsoft YaHei", 11),
                    fg=self.colors['text'], bg=self.colors['bg_card'],
                    anchor="w").pack(fill=tk.X, padx=20, pady=6)
        
        # 底部结束语
        tk.Label(scroll_frame, text="✨ 愿您今日平安顺遂，万事如意 ✨", 
                font=("Microsoft YaHei", 12, "bold"),
                fg=self.colors['gold'], bg=self.colors['bg_hover']).pack(pady=20)
    
    def get_lunar_date(self, date):
        # 2025年农历基准：2025年1月29日 = 农历乙巳年正月初一
        # 2025年闰六月
        
        # 先检查是否是2025年，使用精确的硬编码数据
        if date.year == 2025:
            # 2025年每月天数: 正月30, 二月29, 三月30, 四月29, 五月30, 六月29, 闰六月29, 七月30, 八月29, 九月30, 十月30, 冬月29, 腊月30
            lunar_2025 = [
                (1, 30, False), (2, 29, False), (3, 30, False), (4, 29, False),
                (5, 30, False), (6, 29, False), (6, 29, True),  # 闰六月
                (7, 30, False), (8, 29, False), (9, 30, False), (10, 30, False),
                (11, 29, False), (12, 30, False)
            ]
            
            # 2025年1月29日 = 正月初一
            base_2025 = datetime(2025, 1, 29)
            offset = (date - base_2025).days
            
            if offset < 0:
                # 2025年1月29日之前属于2024年农历
                return self._get_lunar_2024(date)
            
            # 计算农历月日
            day_count = 0
            for month_num, days, is_leap in lunar_2025:
                if offset < day_count + days:
                    lunar_day = offset - day_count + 1
                    month_str = self.lunar_months[month_num - 1]
                    if is_leap:
                        month_str = "闰" + month_str
                    day_str = self.lunar_days[lunar_day - 1] if lunar_day <= 30 else "三十"
                    return f"{month_str}{day_str}"
                day_count += days
            
            # 超出2025年范围
            return "日期超出范围"
        
        elif date.year == 2024:
            return self._get_lunar_2024(date)
        else:
            # 其他年份使用简化计算
            return self._get_lunar_general(date)
    
    def _get_lunar_2024(self, date):
        # 2024年农历基准：2024年2月10日 = 农历甲辰年正月初一
        # 2024年无闰月
        lunar_2024 = [
            (1, 30), (2, 30), (3, 29), (4, 30), (5, 29), (6, 30),
            (7, 29), (8, 30), (9, 29), (10, 30), (11, 29), (12, 30)
        ]
        
        base_2024 = datetime(2024, 2, 10)
        offset = (date - base_2024).days
        
        if offset < 0:
            return "日期超出范围"
        
        day_count = 0
        for month_num, days in lunar_2024:
            if offset < day_count + days:
                lunar_day = offset - day_count + 1
                return f"{self.lunar_months[month_num - 1]}{self.lunar_days[lunar_day - 1]}"
            day_count += days
        
        return "日期超出范围"
    
    def _get_lunar_general(self, date):
        # 简化计算，仅供参考
        month_idx = (date.month + 10) % 12
        day_idx = (date.day + 18) % 30
        return f"{self.lunar_months[month_idx]}{self.lunar_days[day_idx]}"
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MysteryFortuneApp()
    app.run()
