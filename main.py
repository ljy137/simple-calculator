import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import requests
 
from general_calc import GeneralCalculatorFrame
from currency_calc import CurrencyCalculatorFrame

INFO = ("Python CTk Calculator v1.0.3"+
        "\n\n제작자: ljy137\nPython & CustomTkinter 활용")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 현재 모드 표시 프레임 클래스
class FixedHeaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"            
        )

        self.option_menu = ctk.CTkOptionMenu(
            self,
            width=100,
            values=["일반", "환율"],
            command=self.option_menu_command
        )
        self.option_menu.set("일반")
        self.option_menu.grid(
            row=0, 
            column=0, 
            sticky="w", 
            padx=10, 
            pady=10
        )

    # 옵션 메뉴 기능 할당
    def option_menu_command(self, choice):
        if choice == "일반":
            self.master.show_general_calculator()
        elif choice == "환율":
            self.master.show_currency_calculator()


# 메인 앱 클래스
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python CTk Calculator")
        self.geometry("320x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = FixedHeaderFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        self.current_frame = None
        self.frame_general_calc = GeneralCalculatorFrame(self)
        self.frame_currency_calc = CurrencyCalculatorFrame(self)

        self.setup_menu()
        self.switch_frame(self.frame_general_calc)

    # 프레임 변경
    def switch_frame(self, next_frame):

        if self.current_frame is not None:
            self.current_frame.grid_forget()

        self.current_frame = next_frame
        self.current_frame.grid(row=1, column=0, sticky="nsew")

    # 메뉴바 생성
    def setup_menu(self):
        self.menubar = tk.Menu(self)

        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="설정", menu=self.settings_menu)

        self.theme_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label="테마 변경", menu=self.theme_menu)

        self.theme_menu.add_command(
            label="라이트 모드", 
            command=lambda: ctk.set_appearance_mode("Light")
        )
        self.theme_menu.add_command(
            label="다크 모드", 
            command=lambda: ctk.set_appearance_mode("Dark")
        )

        self.theme_menu.add_separator()
        self.theme_menu.add_command(
            label="시스템 설정", 
            command=lambda: ctk.set_appearance_mode("System")
        )

        self.info_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="정보", menu=self.info_menu)
        self.info_menu.add_command(
            label="계산기 정보", 
            command=lambda: messagebox.showinfo("정보", INFO))

        self.config(menu=self.menubar)

    # 일반 계산기로 이동
    def show_general_calculator(self):
        self.switch_frame(self.frame_general_calc)

    # 환율 계산기로 이동
    def show_currency_calculator(self):
        self.switch_frame(self.frame_currency_calc)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()