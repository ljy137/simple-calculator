import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")



# 일반 계산기 프레임 클래스
class GeneralCalculatorFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.input_display = ctk.CTkEntry(
            self,
            placeholder_text="0",
            height=50,
            corner_radius=10,
            border_width=2,
            font=("Arial", 20),
            justify='right'
        )
        
        self.input_display.grid(
            row=0, 
            column=0, 
            columnspan=4, 
            sticky="nsew", 
            padx=10, 
            pady=10
        )

        self.output_display= ctk.CTkLabel(
            self, 
            text="",
            height=40,
            font=("Arial", 30), 
            anchor="e"
        )

        self.output_display.grid(
            row=1, 
            column=0, 
            columnspan=4, 
            sticky="nsew", 
            padx=10, 
            pady=(0, 10)
        )

        self.btn_ac = self.create_btn("AC", lambda: self.button_all_delete(), 2, 0, color="#E74C3C")
        self.create_btn("^", lambda: self.button_click("^"), 2, 1, color="#5D6D7E")
        self.create_btn("÷", lambda: self.button_click("÷"), 2, 2, color="#5D6D7E")
        self.create_btn("←", lambda: self.button_delete(), 2, 3, color="#5D6D7E")

        self.create_btn("7", lambda: self.button_click(7), 3, 0)
        self.create_btn("8", lambda: self.button_click(8), 3, 1)
        self.create_btn("9", lambda: self.button_click(9), 3, 2)
        self.create_btn("x", lambda: self.button_click("x"), 3, 3, color="#3498DB")

        self.create_btn("4", lambda: self.button_click(4), 4, 0)
        self.create_btn("5", lambda: self.button_click(5), 4, 1)
        self.create_btn("6", lambda: self.button_click(6), 4, 2)
        self.create_btn("-", lambda: self.button_click("-"), 4, 3, color="#3498DB")

        self.create_btn("1", lambda: self.button_click(1), 5, 0)
        self.create_btn("2", lambda: self.button_click(2), 5, 1)
        self.create_btn("3", lambda: self.button_click(3), 5, 2)
        self.create_btn("+", lambda: self.button_click("+"), 5, 3, color="#3498DB")

        self.create_btn("0", lambda: self.button_click(0), 6, 0, colspan=2)
        self.create_btn(".", lambda: self.button_click("."), 6, 2)
        self.create_btn("=", lambda: self.button_result(), 6, 3, color="#2ECC71")

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        for i in range(2, 7):
            self.grid_rowconfigure(i, weight=1)

        self.bind('<Configure>', self.resize_fonts)


    # 버튼 생성 함수
    def create_btn(self, text, cmd, row, col, colspan=1, color=None):
        btn = ctk.CTkButton(
            self,
            text=text,
            command=cmd,
            fg_color=color,
            text_color=("gray90", "gray10"),
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

    # 버튼 클릭 이벤트 함수
    def button_click(self, c):
        operators = ["+", "-", "x", "÷", "^"]
        errors = [
            "Error: 계산 범위 초과",
            "Error: 0으로 나눌 수 없음",
            "Error: 잘못된 수식"
        ]

        if c in operators:
            current_result = self.output_display.cget("text")

            if current_result and current_result not in errors:
                self.input_display.delete(0, "end")
                self.input_display.insert("insert", current_result+c)
                self.output_display.configure(text="")

            else:
                self.output_display.configure(text="")
                self.input_display.insert("insert", str(c))

        else:
            self.output_display.configure(text="")
            self.input_display.insert("insert", str(c))

        self.input_display.xview_moveto(1.0)

    # 입력된 값을 전부 삭제하는 함수
    def button_all_delete(self):
        self.output_display.configure(text="")
        self.input_display.delete(0, "end")

    # 입력된 값에서 한 칸 삭제하는 함수
    def button_delete(self):
        self.output_display.configure(text="")
        cursor_pos = self.input_display.index("insert")
        if cursor_pos > 0:
            self.input_display.delete(cursor_pos - 1, cursor_pos)

    # 연산 결과를 출력하는 함수
    def button_result(self):
        try:
            expr = self.input_display.get()
            expr = expr.replace('÷', '/')
            expr = expr.replace('x', '*')
            expr = expr.replace('^', '**')
            
            tmp = eval(expr)
            result = f"{tmp:.4f}"

            if result.endswith(".0000"):
                result = int(tmp)

            self.output_display.configure(text=str(result))
            
        except OverflowError:
            self.output_display.configure(text="Error: 계산 범위 초과")
            
        except ZeroDivisionError:
            self.output_display.configure(text="Error: 0으로 나눌 수 없음")

        except Exception:
            self.output_display.configure(text="Error: 잘못된 수식")

    # 창의 크기에 따라 글자 크기를 최적화하는 함수
    def resize_fonts(self, event):
        
        # 창의 크기가 변할 시 event.widget은
        # .!generalcalculatorframe.!ctkcanvas 를 출력
        # 이후에 문제 생길 경우 이 부분 확인 필요
        if str(event.widget).endswith(".!ctkcanvas"):
            diagonal = math.sqrt(event.width**2 + event.height**2)

            actual_btn_h = int(self.btn_ac.winfo_height())
            new_size = max(20, min(int(actual_btn_h*0.8), int(diagonal/25))) 

            new_input_h = int(event.height * 0.12)
            new_output_h = int(event.height * 0.08)

            self.input_display.configure(font=("Arial", new_size), height=new_input_h)
            self.output_display.configure(font=("Arial", new_size*1.5), height=new_output_h)
            
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(font=("Arial", new_size))


# 환율 계산기 프레임 클래스
class CurrencyCalculatorFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


# 메인 앱 클래스
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python CTk Calculator")
        self.geometry("320x480")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_frame = None

        self.frame_general_calc = GeneralCalculatorFrame(self)
        self.frame_currency_calc = CurrencyCalculatorFrame(self)

        self.setup_menu()
        self.switch_frame(self.frame_general_calc)

    # 프레임 변경 함수
    def switch_frame(self, next_frame):

        if self.current_frame is not None:
            self.current_frame.grid_forget()

        self.current_frame = next_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # 메뉴바 생성 함수
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
            command=lambda: messagebox.showinfo(
                "정보", 
                "Python CTk Calculator v1.0.1\n\n제작자: ljy137\nPython & CustomTkinter 활용")
        )

        self.config(menu=self.menubar)

    # 일반 계산기로 이동하는 함수
    def show_general_calculator(self):
        self.switch_frame(self.frame_general_calc)

    # 환율 계산기로 이동하는 함수
    def show_currency_calculator(self):
        self.switch_frame(self.frame_currency_calc)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()