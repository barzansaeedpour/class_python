import tkinter as tk

# توابع پایه عملیات
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "خطا"
    return a / b

# تابع محاسبه ساده
def calculate(expr):
    """محاسبه عبارت ساده بدون eval"""
    numbers = []
    operators = []

    i = 0
    while i < len(expr):
        if expr[i].isdigit() or expr[i] == '.':
            num_str = ''
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num_str += expr[i]
                i += 1
            numbers.append(float(num_str))
        else:
            operators.append(expr[i])
            i += 1

    # اول ضرب و تقسیم
    i = 0
    while i < len(operators):
        if operators[i] == '*':
            numbers[i] = multiply(numbers[i], numbers[i+1])
            del numbers[i+1]
            del operators[i]
        elif operators[i] == '/':
            numbers[i] = divide(numbers[i], numbers[i+1])
            del numbers[i+1]
            del operators[i]
        else:
            i += 1

    # بعد جمع و تفریق
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result = add(result, numbers[i+1])
        elif op == '-':
            result = subtract(result, numbers[i+1])

    return result

# کلاس ماشین حساب Tkinter
class SimpleCalculator:
    def __init__(self, master):
        self.master = master
        master.title("ماشین حساب ساده")
        self.expression = ""

        self.text_var = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.text_var, font=("Arial", 20), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

        buttons = [
            ('7',1,0),('8',1,1),('9',1,2),('/',1,3),
            ('4',2,0),('5',2,1),('6',2,2),('*',2,3),
            ('1',3,0),('2',3,1),('3',3,2),('-',3,3),
            ('0',4,0),('.',4,1),('C',4,2),('+',4,3),
            ('=',5,0,4)
        ]

        for (text, row, col, colspan) in [(*b,1) if len(b)==3 else b for b in buttons]:
            button = tk.Button(master, text=text, font=("Arial",18), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew")

        for i in range(6):
            master.rowconfigure(i, weight=1)
        for i in range(4):
            master.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "=":
            try:
                self.expression = str(calculate(self.expression))
            except:
                self.expression = "خطا"
        else:
            self.expression += char
        self.text_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = SimpleCalculator(root)
    root.mainloop()
