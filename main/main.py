import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def process_excel(file_path): #Функция для обработки файла
    #Загружаем данные из Excel
    df = pd.read_excel(file_path)
    #Преобразуем столбцы
    df.columns = ['Date', 'Expenses', 'Incomes']
    df['Date'] = pd.to_datetime(df['Date'])
    #Для подсчета доступной суммы на начало дня
    available_balance_start = 0
    result = []
    for date, group in df.groupby('Date'):
        #Сумма всех поступлений и трат за день
        total_operations = group['Expenses'].sum() + group['Incomes'].sum()
        #Доступная сумма на конец дня
        available_balance_end = available_balance_start + total_operations
        result.append([date, available_balance_start, total_operations, available_balance_end])
        #Обновляем доступную сумму на начало следующего дня
        available_balance_start = available_balance_end
    #Создаем таблицу для результатов
    result_df = pd.DataFrame(result, columns=['Date', 'Budget', 'Transactions', 'Residual'])
    #Сохраняем в CSV
    result_df.to_csv('output.csv', index=False)

###Решила добавить небольшой фронт для удобства###

#Открываем файл
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            process_excel(file_path)
            messagebox.showinfo("Успех", "Файл успешно обработан и сохранен как output.csv")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработки файла: {e}")

#Создаем внешний интерфейс
def create_gui():
    root = tk.Tk()
    root.title("Данные по транзакциям")
    open_button = tk.Button(root, text="Открыть файл", command=open_file)
    open_button.pack(pady=20)
    root.geometry("300x150")
    root.mainloop()

# Запуск интерфейса
if __name__ == "__main__":
    create_gui()