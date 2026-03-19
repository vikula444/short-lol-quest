import tkinter as tk
from tkinter import messagebox
from typing import Self

# Исходные данные игры
cor = [
    {'place': 'комната', 'description': 'Вы находитесь в небольшой комнате. На столе лежит книга.', 'actions': [
        {'description': 'осмотреть стол', 'actions': [
            {'description': 'взять стакан'},
            {'description': 'выйти из комнаты', 'actions': [
                {'description': 'возьми отвёртку', 'actions': [
                    {'description': 'открыть вентиляцию и залесть в неё', 'actions': [
                        {'description': 'ползти влево', 'actions': [
                            {'description': 'проиграл'}
                        ]}
                    ]}
                ]}
            ]}
        ]},
        {'description': 'подойти к окну', 'actions': [
            {'description': 'открыть окно', 'actions': [
                {'description': 'спрыгнуть', 'actions': [
                    {'description': 'тебе повезло, первый этаж - ТЫ ВЫЖИЛ И УБЕЖАЛ В ЛЕС'}
                ]}
            ]}
        ]}
    ]}
]


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовая игра")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.current_node = cor[0]
        self.history = []  # для возврата к предыдущим состояниям

        # доздание интерфейса
        self.create_widgets()

        # 0тображение начальной локации
        self.show_location()

    def create_widgets(self):
        # текстовое поле для описания
        self.description_text = tk.Text(self.root, height=8, width=70, wrap=tk.WORD, state=tk.DISABLED)
        self.description_text.pack(pady=10)

        # рамка для кнопок действий
        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack(pady=10)

        # кнопка возврата 
        self.back_button = tk.Button(self.root, text="начать заново", command=self.restart_game, state=tk.NORMAL)
        self.back_button.pack(pady=5)

    def show_location(self):
        # очистка текстового поля
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)

        if 'place' in self.current_node:
            self.description_text.insert(tk.END, f"локация: {self.current_node['place']}\n\n")
        self.description_text.insert(tk.END, self.current_node['description'])

        # если есть описание проигрыша или победы
        if 'description' in self.current_node and ('проиграл' in self.current_node['description'] or
                                                   'ВЫЖИЛ' in self.current_node['description']):
            self.description_text.insert(tk.END, f"\n\n{self.current_node['description']}")

        self.description_text.config(state=tk.DISABLED)

        # очистка старых кнопок 
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        # создание новых кнопок действий
        if 'actions' in self.current_node:
            for action in self.current_node['actions']:
                btn = tk.Button(self.actions_frame, text=action['description'],
                                command=lambda a=action: self.perform_action(a))
                btn.pack(pady=2, padx=10, fill=tk.X)

        # если это конец игры (проигрыш или победа)
        if 'description' in self.current_node and ('проиграл' in self.current_node['description'] or
                                                   'ВЫЖИЛ' in self.current_node['description']):
            self.back_button.config(text="начать заново", state=tk.NORMAL)
        else:
            self.back_button.config(state=tk.DISABLED)

    def perform_action(self, action):
        self.history.append(self.current_node)
        # переходим к следующему узлу
        if 'actions' in action:
            self.current_node = action
            self.show_location()
        elif 'description' in action:
            self.current_node = action
            self.show_location()

    def restart_game(self):
        """перезапуск игры с начала"""
        self.current_node = cor[0]
        self.history = []
        self.show_location()


def main():
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()
