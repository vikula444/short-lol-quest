import tkinter as tk
from datetime import datetime
import os

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
        self.root.title("текстовая игра")
        self.root.geometry("600x400")
        self.current_node = cor[0]
        
        # счетчики действий побед поражений
        self.action_count = 0
        self.win_count = 0
        self.loss_count = 0
        
        # нач. лог
        if not os.path.exists("logs"):
            os.makedirs("logs")
        self.log_file = open("logs/game_log.txt", "w", encoding="utf-8")
        
        self.create_widgets()
        self.show_location()

    def log(self, msg):
        self.log_file.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_file.flush()

       #создание основных эл-ов интерфейса
    def create_widgets(self):
        self.text = tk.Text(self.root, height=8, width=70, wrap=tk.WORD, state=tk.DISABLED)
        self.text.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.back_btn = tk.Button(self.root, text="начать заново", command=self.restart_game, state=tk.DISABLED)
        self.back_btn.pack(pady=5) #кнопка лля перезапуска игры в начале отключена

    def show_location(self): #обнов текст поля
        self.text.config(state=tk.NORMAL) #реж редакт
        self.text.delete(1.0, tk.END) #очищение текст поля

        if 'place' in self.current_node: 
            self.text.insert(tk.END, f"локация: {self.current_node['place']}\n\n") 
        self.text.insert(tk.END, self.current_node['description'])

        self.text.config(state=tk.DISABLED)

        for btn in self.frame.winfo_children(): #делет предыдущ кнопки перед созданием нью кнопок
            btn.destroy()

        if 'actions' in self.current_node:
            for action in self.current_node['actions']:
                btn = tk.Button(self.frame, text=action['description'],
                               command=lambda a=action: self.do_action(a)) #передача текущ значения переменной
                btn.pack(pady=2, fill=tk.X)

        if 'description' in self.current_node:
            if 'проиграл' in self.current_node['description']:
                self.loss_count += 1 #увеличение  счетчика поражений
                self.log(f"поражение ({self.loss_count})")
                self.save_stats()
                self.back_btn.config(state=tk.NORMAL)
            elif 'ВЫЖИЛ' in self.current_node['description']:
                self.win_count += 1
                self.log(f"Победа ({self.win_count})")
                self.save_stats()
                self.back_btn.config(state=tk.NORMAL)
            else:
                self.back_btn.config(state=tk.DISABLED)

    def do_action(self, action):
        self.action_count += 1 # в моем коде это нужно чтобы отслеживать колво действий и описаний
        self.log(f"{self.action_count}: {action['description']}")
        self.current_node = action # обновление текущ состояния игры
        self.show_location() #обновление интерфейса

    def save_stats(self):
        with open("stats.txt", "w") as f:
            f.write(f"побед: {self.win_count}\n")
            f.write(f"Поражений: {self.loss_count}\n")
            f.write(f"действий: {self.action_count}\n")

    def restart_game(self):
        self.log(f"перезапуск")
        self.action_count = 0
        self.current_node = cor[0]
        self.show_location()


root = tk.Tk()
game = GameGUI(root)
root.mainloop()
