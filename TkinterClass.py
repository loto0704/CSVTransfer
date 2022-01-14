#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter.constants import FLAT, MULTIPLE, SOLID
import tkinter.filedialog, datetime, os, pandas, json

class TkinterClass:
    def __init__(self) -> None:
        root = tkinter.Tk()
        root.title("CSV変換ツール")
        root.geometry("500x500")
        
        # CSVファイル選択
        button_csv = tkinter.Button(root, text='CSVファイル選択', font=('', 20),
                           width=24, height=1, bg='#999999', activebackground="#aaaaaa")
        button_csv.bind('<ButtonPress>', self.csv_file_dialog)
        button_csv.pack(pady=40)
        
        self.csv_file_name = tkinter.StringVar()
        self.csv_file_name.set('未選択です')
        label_csv_file_select = tkinter.Label(textvariable=self.csv_file_name, font=('', 10))
        label_csv_file_select.pack(pady=0)
        
        self.column_name = tkinter.StringVar()
        label_file_path = tkinter.Label(textvariable=self.column_name, font=('', 9))
        label_file_path.pack(pady=0)
        
        # jsonファイル選択
        button_json = tkinter.Button(root, text='jsonファイル選択', font=('', 20),
                           width=24, height=1, bg='#999999', activebackground="#aaaaaa")
        button_json.bind('<ButtonPress>', self.json_file_dialog)
        button_json.pack(pady=40)
        
        self.json_file_name = tkinter.StringVar()
        self.json_file_name.set('未選択です')
        label_json_file_select = tkinter.Label(textvariable=self.json_file_name, font=('', 10))
        label_json_file_select.pack(pady=0)
        
        root.mainloop()
    
    def csv_file_dialog(self, event):
        'CSVファイルダイアログ'
        fTyp = [("", ".csv")]
        csv_file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp)
        
        if self.csv_file_name == "":
            self.csv_file_name.set('CSVファイルが未選択です')
            return
        else:
            self.csv_file_name.set(csv_file_name)
        
        proceed_button = tkinter.Button(text='変換実行',font=('', 15),
                                width=12, height=1, bg='#999999', activebackground="#aaaaaa")
        proceed_button.bind('<ButtonPress>', self.transform_proceed)
        proceed_button.pack(pady=40)
        
    def json_file_dialog(self, event):
        'jsonファイルダイアログ'
        fTyp = [("", ".json")]
        json_file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp)
        
        if self.json_file_name == "":
            self.json_file_name.set('jsonファイルが未選択です')
            return
        else:
            self.json_file_name.set(json_file_name)
        
        
        
    def transform_proceed(self, event):
        now = datetime.datetime.now()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        read_df = pandas.read_csv(self.csv_file_name.get(), encoding='utf-8')
        json_open = open(file=self.json_file_name.get(), mode='r', encoding='utf-8')
        # with open(file=self.json_file_name.get(), mode='r') as json_open:
        format_json = json.load(json_open)["Transfer-column"]
        # print(len(format_json))
        # list_get = self.label_list_column.curselection()
        json_keys = []
        csv_column = []
        for i in range(len(format_json)):
            for j in format_json[i].keys():
                json_keys.append(j)
            
        out_df = read_df.loc[:,json_keys]
        for i in range(len(json_keys)):
            # flag = "replace-str" in format_json[i][json_keys[i]]
            if "replace-str" in format_json[i][json_keys[i]]:
                out_df[json_keys[i]] = out_df[json_keys[i]].str.replace(format_json[i][json_keys[i]]["replace-str"][0], format_json[i][json_keys[i]]["replace-str"][1])
            
        out_df.to_csv(f'{base_dir}/output{now.strftime("%Y%m%d-%H%M%S")}.csv', header=True,index=False)
        # return save_df
        
        # 終了
        quit()
    
    def close(self, event):
        # 閉じる
        quit()
