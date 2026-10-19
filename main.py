from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
import json
import os

# 注册中文字体，解决手机端中文乱码
LabelBase.register(name="CNFont", fn_regular="DroidSansFallback.ttf")

# 数据文件
DATA_FILE = "records.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 页面1：记账录入
class RecordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        self.input_money = TextInput(hint_text="输入金额", font_name="CNFont", font_size=20, input_filter="float")
        self.input_type = TextInput(hint_text="类型：吃饭/交通/工资等", font_name="CNFont", font_size=20)
        self.input_note = TextInput(hint_text="备注", font_name="CNFont", font_size=20)

        btn_in = Button(text="✅ 收入", font_name="CNFont", font_size=20, background_color=(0.2,0.8,0.2,1))
        btn_out = Button(text="❌ 支出", font_name="CNFont", font_size=20, background_color=(0.9,0.2,0.2,1))
        btn_in.bind(on_press=self.add_income)
        btn_out.bind(on_press=self.add_outcome)

        layout.add_widget(Label(text="📝 记一笔账", font_name="CNFont", font_size=26))
        layout.add_widget(self.input_money)
        layout.add_widget(self.input_type)
        layout.add_widget(self.input_note)

        btn_box = BoxLayout(spacing=20)
        btn_box.add_widget(btn_in)
        btn_box.add_widget(btn_out)
        layout.add_widget(btn_box)
        self.add_widget(layout)

    def add_income(self, *args):
        self.save_record(1)
    def add_outcome(self, *args):
        self.save_record(-1)

    def save_record(self, sign):
        money_text = self.input_money.text.strip()
        if not money_text:
            return
        record = {
            "money": float(money_text)*sign,
            "type": self.input_type.text,
            "note": self.input_note.text
        }
        data = load_data()
        data.append(record)
        save_data(data)
        # 清空输入框
        self.input_money.text = ""
        self.input_type.text = ""
        self.input_note.text = ""

# 页面2：明细列表
class ListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.label_title = Label(text="📋 全部收支明细", font_name="CNFont", font_size=24)
        self.scroll = ScrollView()
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter('height'))
        self.scroll.add_widget(self.list_box)
        self.btn_refresh = Button(text="🔄刷新", font_name="CNFont", size_hint_y=0.15)
        self.btn_refresh.bind(on_press=self.refresh)
        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.btn_refresh)
        self.add_widget(self.layout)
        self.refresh()

    def refresh(self, *args):
        self.list_box.clear_widgets()
        data = load_data()
        for r in reversed(data):
            txt = f"{r['type']} | {r['money']} | {r['note']}"
            lbl = Label(text=txt, font_name="CNFont", size_hint_y=None, height=44)
            self.list_box.add_widget(lbl)

# 页面3：统计页面
class StatScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20)
        self.label_text = Label(text="📊收支统计", font_name="CNFont", font_size=26)
        self.result_label = Label(text="", font_name="CNFont", font_size=20)
        btn_calc = Button(text="计算统计", font_name="CNFont", size_hint_y=0.2)
        btn_calc.bind(on_press=self.calc)
        layout.add_widget(self.label_text)
        layout.add_widget(self.result_label)
        layout.add_widget(btn_calc)
        self.add_widget(layout)

    def calc(self,*args):
        data = load_data()
        total_in = sum(i["money"] for i in data if i["money"]>0)
        total_out = abs(sum(i["money"] for i in data if i["money"]<0))
        balance = total_in - total_out
        self.result_label.text = f"总收入：{total_in:.2f}\n总支出：{total_out:.2f}\n结余：{balance:.2f}"

# 主界面（包含底部导航）
class MainLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.sm = ScreenManager()
        self.sm.add_widget(RecordScreen(name="record"))
        self.sm.add_widget(ListScreen(name="list"))
        self.sm.add_widget(StatScreen(name="stat"))

        # 底部导航栏
        nav_box = BoxLayout(size_hint_y=0.15)
        btn1 = Button(text="记账", font_name="CNFont")
        btn2 = Button(text="明细", font_name="CNFont")
        btn3 = Button(text="统计", font_name="CNFont")
        btn1.bind(on_press=lambda x: setattr(self.sm, "current", "record"))
        btn2.bind(on_press=lambda x: setattr(self.sm, "current", "list"))
        btn3.bind(on_press=lambda x: setattr(self.sm, "current", "stat"))
        nav_box.add_widget(btn1)
        nav_box.add_widget(btn2)
        nav_box.add_widget(btn3)

        self.add_widget(self.sm)
        self.add_widget(nav_box)

class AccountBookApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    AccountBookApp().run()
