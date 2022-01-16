#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter.constants import FLAT, MULTIPLE, SOLID
import tkinter.filedialog
import datetime, os, pandas, json, re


class TkinterClass:
    def __init__(self) -> None:
        root = tkinter.Tk()
        root.title("CSV変換ツール")
        root.geometry("500x500")
        
        # CSVファイル選択
        button_csv = tkinter.Button(root, text='CSVファイル選択', font=('', 20), width=24, height=1)
        button_csv.bind('<ButtonPress>', self.csv_file_dialog)
        button_csv.pack(pady=40)

        # CSVファイル名表示
        self.csv_file_name = tkinter.StringVar()
        self.csv_file_name.set('未選択です')
        label_csv_file_select = tkinter.Label(textvariable=self.csv_file_name, font=('', 10))
        label_csv_file_select.pack(pady=0)
        
        # jsonファイル選択
        button_json = tkinter.Button(root, text='jsonファイル選択', font=('', 20), width=24, height=1)
        button_json.bind('<ButtonPress>', self.json_file_dialog)
        button_json.pack(pady=40)

        # jsonファイル名表示
        self.json_file_name = tkinter.StringVar()
        self.json_file_name.set('未選択です')
        label_json_file_select = tkinter.Label(textvariable=self.json_file_name, font=('', 10))
        label_json_file_select.pack(pady=0)

        root.mainloop()

    def proceed(self):
        # 実行ボタン
        if self.csv_file_name.get() != '未選択です':
            proceed_button = tkinter.Button(text='変換実行', font=('', 15),
                                            width=12, height=1, activebackground="#aaaaaa")
            proceed_button.bind('<ButtonPress>', self.transform_proceed)
            proceed_button.pack(pady=40)
    
    def csv_file_dialog(self, event):
        'CSVファイルダイアログ'
        fTyp = [("", ".csv")]
        csv_file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp)
        
        if self.csv_file_name == "":
            self.csv_file_name.set('CSVファイルが未選択です')
            return
        else:
            self.csv_file_name.set(csv_file_name)
            # 実行ボタン
            if self.json_file_name.get() != '未選択です':
                proceed_button = tkinter.Button(text='変換実行', font=('', 15),
                                                width=12, height=1, activebackground="#aaaaaa")
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
            # 実行ボタン
            if self.csv_file_name.get() != '未選択です':
                proceed_button = tkinter.Button(text='変換実行', font=('', 15),
                                                width=12, height=1, activebackground="#aaaaaa")
                proceed_button.bind('<ButtonPress>', self.transform_proceed)
                proceed_button.pack(pady=40)
        
    def transform_proceed(self, event):
        read_df = pandas.read_csv(self.csv_file_name.get(), encoding='utf-8') # CSV読み込み
        json_open = open(file=self.json_file_name.get(), mode='r', encoding='utf-8') # フォーマット読み込み
        json_load = json.load(json_open)
        add_column = json_load["Save-column"]
        format_json = json_load["Transfer-column"]
        out_df = read_df.loc[:, add_column]
        # Transfer-column内の要素を数える
        json_keys = []
        for i in range(len(format_json)):
            for j in format_json[i].keys():
                json_keys.append(j)

        # データフレームに入れたデータをフォーマットに従って変換
        for i in range(len(json_keys)):
            # フィルター
            if "Filter" in format_json[i][add_column[i]]:
                out_df = out_df[out_df[add_column[i]] == format_json[i][add_column[i]]["Filter"]]

            # フィルター（複数）
            if "Filters" in format_json[i][add_column[i]]:
                out_df = out_df[out_df[add_column[i]].isin(format_json[i][add_column[i]]["Filters"])]

            # 指定文字内抜き出し
            if "extract" in format_json[i][add_column[i]]:
                for j in range(len(out_df)):
                    out_df[add_column[i]][j] = \
                        re.findall(
                            f"{format_json[i][add_column[i]]['extract'][0]}(.*){format_json[i][add_column[i]]['extract'][1]}",
                            out_df[add_column[i]][j])[0]

            # 指定文字以前抜き出し
            if "extract-before" in format_json[i][add_column[i]]:
                for j in range(len(out_df)):
                    out_df[add_column[i]][j] = \
                        re.findall(f"(.*){format_json[i][add_column[i]]['extract-before']}",
                                   out_df[add_column[i]][j])[0]

            # 指定文字以降抜き出し
            if "extract-after" in format_json[i][add_column[i]]:
                for j in range(len(out_df)):
                    out_df[add_column[i]][j] = \
                        re.findall(f"{format_json[i][add_column[i]]['extract-after']}(.*)",
                                   out_df[add_column[i]][j])[0]

            # 文字列置換
            if "replace-str" in format_json[i][add_column[i]]:
                out_df[add_column[i]] = \
                    out_df[add_column[i]].str.replace(
                    format_json[i][add_column[i]]["replace-str"][0],
                    format_json[i][add_column[i]]["replace-str"][1])

        # データを保存
        base_dir = os.path.abspath(os.path.dirname(__file__))
        now = datetime.datetime.now()
        out_df.to_csv(f'{base_dir}/output{now.strftime("%Y%m%d-%H%M%S")}.csv', header=True, index=False)
        # return save_df
        
        # 終了
        quit()
    
    def close(self, event):
        # 閉じる
        quit()


if __name__ == "__main__":
    TkinterClass()
