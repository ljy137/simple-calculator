import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import requests

# 환율 계산기 프레임 클래스
class CurrencyCalculatorFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.currency_map = {
            "원 - ₩": "KRW",
            "달러 - $": "USD",
            "엔 - 円": "JPY",
            "유로 - €": "EUR",
            "위안 - ¥": "CNY",
            "루피 - ₹": "INR"
        }

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.currency_option_menu1 = ctk.CTkOptionMenu(
            self,
            width=100,
            values=[
                "원 - ₩", 
                "달러 - $", 
                "엔 - 円", 
                "유로 - €", 
                "위안 - ¥",
                "루피 - ₹"
            ]
        )
        self.currency_option_menu1.set("원 - ₩")
        self.currency_option_menu1.grid(
            row=0, 
            column=0, 
            sticky="w", 
            padx=10, 
            pady=10
        )

        self.input_display = ctk.CTkEntry(
            self,
            placeholder_text="0",
            height=20,
            corner_radius=10,
            border_width=2,
            font=("Arial", 20),
            justify='right'
        )
        self.input_display.grid(
            row=0, 
            column=1, 
            columnspan=2,
            sticky="ew", 
            padx=10, 
            pady=10
        )

        self.currency_option_menu2 = ctk.CTkOptionMenu(
            self,
            width=100,
            values=[
                "원 - ₩", 
                "달러 - $", 
                "엔 - 円", 
                "유로 - €", 
                "위안 - ¥",
                "루피 - ₹"
            ]
        )
        self.currency_option_menu2.set("달러 - $")
        self.currency_option_menu2.grid(
            row=1, 
            column=0, 
            sticky="w", 
            padx=10, 
            pady=10
        )

        self.output_display = ctk.CTkLabel(
            self,
            text="",
            height=20,
            font=("Arial", 20),
            justify='right'
        )
        self.output_display.grid(
            row=1, 
            column=1,
            columnspan=2,
            sticky="e", 
            padx=10, 
            pady=10
        )

        self.currency_info_display = ctk.CTkLabel(
            self,
            text="",
            height=50,
            font=("Arial", 15),
            justify='left'
        )
        self.currency_info_display.grid(
            row=2, 
            column=0,
            columnspan=3,
            sticky="w", 
            padx=10, 
            pady=10
        )

        self.btn_ac = self.create_btn("AC", lambda: self.button_all_delete(), 3, 0, colspan=2, color="#E74C3C")
        self.create_btn("←", lambda: self.button_delete(), 3, 2, color="#5D6D7E")

        self.create_btn("7", lambda: self.button_click(7), 4, 0)
        self.create_btn("8", lambda: self.button_click(8), 4, 1)
        self.create_btn("9", lambda: self.button_click(9), 4, 2)
        
        self.create_btn("4", lambda: self.button_click(4), 5, 0)
        self.create_btn("5", lambda: self.button_click(5), 5, 1)
        self.create_btn("6", lambda: self.button_click(6), 5, 2)
        
        self.create_btn("1", lambda: self.button_click(1), 6, 0)
        self.create_btn("2", lambda: self.button_click(2), 6, 1)
        self.create_btn("3", lambda: self.button_click(3), 6, 2)
        
        self.create_btn("0", lambda: self.button_click(0), 7, 0)
        self.create_btn(".", lambda: self.button_click("."), 7, 1)
        self.create_btn("=", lambda: self.button_result(), 7, 2, color="#2ECC71")
        
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i in range(3, 8):
            self.grid_rowconfigure(i, weight=1)

        self.bind('<Configure>', self.resize_fonts)


    # frankfurter API를 호출하여 실시간으로 환율정보를 가져와 계산
    def exchange_rate_calculate(self):
        from_currency = self.currency_map[self.currency_option_menu1.get()]
        to_currency = self.currency_map[self.currency_option_menu2.get()]

        if from_currency == to_currency:
            self.output_display.configure(text=str(self.input_display.get()))
            self.currency_info_display.configure(text="동일한 통화입니다.")
            return
        
        try:
            url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
            response = requests.get(url)
            data = response.json()
            exchange_rate = data['rates'][to_currency]
            
            input_values = float(self.input_display.get())
            result = float(input_values)*exchange_rate
            self.output_display.configure(text=f"{result:,.2f}")
            self.currency_info_display.configure(text=f"1{from_currency} = {exchange_rate}{to_currency}\n최신 업데이트 : {data["date"]}")
        
        except ValueError:
            self.output_display.configure(text="")
            self.currency_info_display.configure(text="올바른 숫자 형식이 아닙니다.")

        except Exception as e:
            print(f"연결 안 됨: {e}")

    # 버튼 생성
    def create_btn(self, text, cmd, row, col, colspan=1, color=None):
        btn = ctk.CTkButton(
            self,
            text=text,
            command=cmd,
            fg_color=color,
            text_color="gray90",
            corner_radius=8,
            hover_color="#3B3B3B" if not color else None
        )

        btn.grid(
            row=row, 
            column=col, 
            columnspan=colspan, 
            sticky="nsew", 
            padx=3, 
            pady=3
        )

        return btn

    # 버튼 클릭 이벤트 처리
    def button_click(self, c):
        self.output_display.configure(text="")
        self.input_display.insert("insert", str(c))
        self.input_display.xview_moveto(1.0)

    # 입력된 값을 전부 삭제
    def button_all_delete(self):
        self.output_display.configure(text="")
        self.input_display.delete(0, "end")

    # 입력된 값에서 한 칸 삭제
    def button_delete(self):
        self.output_display.configure(text="")
        cursor_pos = self.input_display.index("insert")
        if cursor_pos > 0:
            self.input_display.delete(cursor_pos - 1, cursor_pos)

    # 연산 결과 출력
    def button_result(self):
        self.exchange_rate_calculate()

    # 창의 크기에 따라 글자 크기 최적화
    def resize_fonts(self, event):
        
        # 창의 크기가 변할 시 event.widget은
        # .!generalcalculatorframe.!ctkcanvas 를 출력
        # 이후에 문제 생길 경우 이 부분 확인 필요
        if str(event.widget).endswith("canvas"):
            diagonal = math.sqrt(event.width**2 + event.height**2)

            actual_btn_h = int(self.btn_ac.winfo_height())
            new_size = max(20, min(int(actual_btn_h*0.8), int(diagonal/25))) 

            new_input_h = int(event.height * 0.12)
            new_output_h = int(event.height * 0.08)

            self.input_display.configure(font=("Arial", new_size), height=new_input_h)
            self.output_display.configure(font=("Arial", new_size), height=new_output_h)
            
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(font=("Arial", new_size))


