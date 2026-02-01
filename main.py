import tkinter as tk

root = tk.Tk()
root.title("Python Calculator")
root.geometry("300x400")

display = tk.Entry(root, borderwidth=5, font=("Arial", 18), justify='right')
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

result_display= tk.Label(root, font=("Arial", 18), anchor="e")
result_display.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

def button_click(c):
    result_display.config(text=str(""))
    display.insert(tk.INSERT, str(c))

def button_all_delete():
    result_display.config(text=str(""))
    display.delete(0, tk.END)

def button_delete():
    result_display.config(text=str(""))
    cursor_pos = display.index(tk.INSERT)
    if cursor_pos > 0:
        display.delete(cursor_pos - 1, cursor_pos)

def button_operation():
    try:
        expr = display.get()
        expr = expr.replace('÷', '/')
        expr = expr.replace('x', '*')
        expr = expr.replace('^', '**')
        
        tmp = eval(expr)
        result = f"{tmp:.2f}"

        if result.endswith(".00"):
            result = int(tmp)

        result_display.config(text=str(result))
        
    except OverflowError:
        result_display.config(text="Error: 계산 범위 초과")
        
    except ZeroDivisionError:
        result_display.config(text="Error: 0으로 나눌 수 없음")

    except Exception:
        result_display.config(text="Error: 잘못된 수식")

btn_ac = tk.Button(root, text="AC", command=lambda: button_all_delete())
btn_power = tk.Button(root, text="^", command=lambda: button_click("^"))
btn_division = tk.Button(root, text="÷", command=lambda: button_click("÷"))
btn_backspace = tk.Button(root, text="<-", command=lambda: button_delete())
btn_multiplication = tk.Button(root, text="x", command=lambda: button_click("x"))
btn_minus = tk.Button(root, text="-", command=lambda: button_click("-"))
btn_plus = tk.Button(root, text="+", command=lambda: button_click("+"))
btn_equal = tk.Button(root, text="=", command=lambda: button_operation())
btn_point = tk.Button(root, text=".", command=lambda: button_click("."))

btn_0 = tk.Button(root, text="0", command=lambda: button_click(0))
btn_1 = tk.Button(root, text="1", command=lambda: button_click(1))
btn_2 = tk.Button(root, text="2", command=lambda: button_click(2))
btn_3 = tk.Button(root, text="3", command=lambda: button_click(3))
btn_4 = tk.Button(root, text="4", command=lambda: button_click(4))
btn_5 = tk.Button(root, text="5", command=lambda: button_click(5))
btn_6 = tk.Button(root, text="6", command=lambda: button_click(6))
btn_7 = tk.Button(root, text="7", command=lambda: button_click(7))
btn_8 = tk.Button(root, text="8", command=lambda: button_click(8))
btn_9 = tk.Button(root, text="9", command=lambda: button_click(9))


btn_ac.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
btn_power.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
btn_division.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
btn_backspace.grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
btn_multiplication.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
btn_minus.grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
btn_plus.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)
btn_equal.grid(row=6, column=3, sticky="nsew", padx=2, pady=2)
btn_point.grid(row=6, column=2, sticky="nsew", padx=2, pady=2)

btn_0.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
btn_1.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
btn_2.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
btn_3.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)
btn_4.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
btn_5.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
btn_6.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
btn_7.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
btn_8.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
btn_9.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)

for i in range(4):
    root.grid_columnconfigure(i, weight=1)

for i in range(2, 7):
    root.grid_rowconfigure(i, weight=1)

def resize_fonts(event):
    new_size = max(10, int(event.width / 20)) 
    display.config(font=("Arial", int(new_size)))
    result_display.config(font=("Arial", int(new_size)))
    
    for child in root.winfo_children():
        if isinstance(child, tk.Button):
            child.config(font=("Arial", new_size))

root.bind('<Configure>', resize_fonts)
root.mainloop()