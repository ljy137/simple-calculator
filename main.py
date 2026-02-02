import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# 버튼 생성 함수
def create_btn(text, cmd, row, col, colspan=1, color=None):
    btn = ctk.CTkButton(
        root,
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
def button_click(c):
    operators = ["+", "-", "x", "÷", "^"]
    errors = [
        "Error: 계산 범위 초과",
        "Error: 0으로 나눌 수 없음",
        "Error: 잘못된 수식"
    ]

    if c in operators:
        current_result = output_display.cget("text")

        if current_result and current_result not in errors:
            input_display.delete(0, "end")
            input_display.insert("insert", current_result+c)
            output_display.configure(text="")

        else:
            output_display.configure(text="")
            input_display.insert("insert", str(c))

    else:
        output_display.configure(text="")
        input_display.insert("insert", str(c))

    input_display.xview_moveto(1.0)

# 입력된 값을 전부 삭제하는 함수
def button_all_delete():
    output_display.configure(text="")
    input_display.delete(0, "end")

# 입력된 값에서 한 칸 삭제하는 함수
def button_delete():
    output_display.configure(text="")
    cursor_pos = input_display.index("insert")
    if cursor_pos > 0:
        input_display.delete(cursor_pos - 1, cursor_pos)

# 연산 결과를 출력하는 함수
def button_result():
    try:
        expr = input_display.get()
        expr = expr.replace('÷', '/')
        expr = expr.replace('x', '*')
        expr = expr.replace('^', '**')
        
        tmp = eval(expr)
        result = f"{tmp:.4f}"

        if result.endswith(".0000"):
            result = int(tmp)

        output_display.configure(text=str(result))
        
    except OverflowError:
        output_display.configure(text="Error: 계산 범위 초과")
        
    except ZeroDivisionError:
        output_display.configure(text="Error: 0으로 나눌 수 없음")

    except Exception:
        output_display.configure(text="Error: 잘못된 수식")

# 창의 크기에 따라 글자 크기를 최적화하는 함수
def resize_fonts(event):
    if event.widget == root:
        diagonal = math.sqrt(event.width**2 + event.width**2)

        actual_btn_h = int(btn_ac.winfo_height())
        new_size = max(20, min(int(actual_btn_h*0.8), int(diagonal/25))) 

        new_input_h = int(event.height * 0.12)
        new_output_h = int(event.height * 0.08)

        input_display.configure(font=("Arial", new_size), height=new_input_h)
        output_display.configure(font=("Arial", new_size*1.5), height=new_output_h)
        
        for child in root.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(font=("Arial", new_size))


root = ctk.CTk()
root.title("Python CTk Calculator")
root.geometry("320x480")

menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="설정", menu=settings_menu)

theme_menu = tk.Menu(settings_menu, tearoff=0)
settings_menu.add_cascade(label="테마 변경", menu=theme_menu)

theme_menu.add_command(
    label="라이트 모드", 
    command=lambda: ctk.set_appearance_mode("Light")
)
theme_menu.add_command(
    label="다크 모드", 
    command=lambda: ctk.set_appearance_mode("Dark")
)

theme_menu.add_separator()
theme_menu.add_command(
    label="시스템 설정", 
    command=lambda: ctk.set_appearance_mode("System")
)

info_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="정보", menu=info_menu)
info_menu.add_command(
    label="계산기 정보", 
    command=lambda: messagebox.showinfo(
        "정보", 
        "Python CTk Calculator v1.0.1\n\n제작자: ljy137\nPython & CustomTkinter 활용")
)

root.config(menu=menubar)


input_display = ctk.CTkEntry(
    root,
    placeholder_text="0",
    height=50,
    corner_radius=10,
    border_width=2,
    font=("Arial", 20),
    justify='right'
)
input_display.grid(
    row=0, 
    column=0, 
    columnspan=4, 
    sticky="nsew", 
    padx=10, 
    pady=10
)

output_display= ctk.CTkLabel(
    root, 
    text="",
    height=40,
    font=("Arial", 30), 
    anchor="e"
)
output_display.grid(
    row=1, 
    column=0, 
    columnspan=4, 
    sticky="nsew", 
    padx=10, 
    pady=(0, 10)
)


btn_ac = create_btn("AC", lambda: button_all_delete(), 2, 0, color="#E74C3C")
create_btn("^", lambda: button_click("^"), 2, 1, color="#5D6D7E")
create_btn("÷", lambda: button_click("÷"), 2, 2, color="#5D6D7E")
create_btn("←", lambda: button_delete(), 2, 3, color="#5D6D7E")

create_btn("7", lambda: button_click(7), 3, 0)
create_btn("8", lambda: button_click(8), 3, 1)
create_btn("9", lambda: button_click(9), 3, 2)
create_btn("x", lambda: button_click("x"), 3, 3, color="#3498DB")

create_btn("4", lambda: button_click(4), 4, 0)
create_btn("5", lambda: button_click(5), 4, 1)
create_btn("6", lambda: button_click(6), 4, 2)
create_btn("-", lambda: button_click("-"), 4, 3, color="#3498DB")

create_btn("1", lambda: button_click(1), 5, 0)
create_btn("2", lambda: button_click(2), 5, 1)
create_btn("3", lambda: button_click(3), 5, 2)
create_btn("+", lambda: button_click("+"), 5, 3, color="#3498DB")

create_btn("0", lambda: button_click(0), 6, 0, colspan=2)
create_btn(".", lambda: button_click("."), 6, 2)
create_btn("=", lambda: button_result(), 6, 3, color="#2ECC71")

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

for i in range(2, 7):
    root.grid_rowconfigure(i, weight=1)

root.bind('<Configure>', resize_fonts)
root.mainloop()