import tkinter
from tkinter.constants import FLAT, MULTIPLE, SOLID
import tkinter.filedialog, datetime, os
import pandas

def main():
    TkinterClass()

class TkinterClass:
    def __init__(self) -> None:
        root = tkinter.Tk()
        root.title("CSV変換ツール")
        root.geometry("500x500")
        
        # ファイル選択
        button = tkinter.Button(root, text='CSVファイル選択', font=('', 20),
                           width=24, height=1, bg='#999999', activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.file_dialog)
        button.pack(pady=40)

        self.file_name = tkinter.StringVar()
        self.file_name.set('未選択です')
        label_file_select = tkinter.Label(textvariable=self.file_name, font=('', 10))
        label_file_select.pack(pady=0)
        
        self.column_name = tkinter.StringVar()
        label_file_path = tkinter.Label(textvariable=self.column_name, font=('', 9))
        label_file_path.pack(pady=0)
        
        self.list_column = tkinter.StringVar()
        label_list_column = tkinter.Listbox(listvariable=self.list_column,
                                       font=('', 9), selectmode=MULTIPLE, relief=FLAT)
        
        root.mainloop()
    
    def file_dialog(self, event):
        'ファイルダイアログ'
        fTyp = [("", ".csv")]
        file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp)
        
        if self.file_name == "":
            self.file_name.set('未選択です')
            return
        else:
            self.file_name.set(file_name)
            
        with open(file=file_name, mode='r', encoding='utf-8-sig') as f:
            self.label_list_column = tkinter.Listbox(listvariable=self.list_column,
                                           font=('', 9), selectmode=MULTIPLE, relief=SOLID)
            self.list_column.set(f.readline().split(','))
            self.label_list_column.pack(pady=0)
            
        proceed_button = tkinter.Button(text='変換実行',font=('', 15),
                                width=12, height=1, bg='#999999', activebackground="#aaaaaa")
        proceed_button.bind('<ButtonPress>', self.transform_proceed)
        proceed_button.pack(pady=40)
        
    def transform_proceed(self, event):
        now = datetime.datetime.now()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        read_df = pandas.read_csv(self.file_name.get(), encoding='utf-8-sig')
        list_get = self.label_list_column.curselection()
        csv_column = []
        for i in range(len(list_get)):
            if "\n" in self.label_list_column.get(list_get[i]):
                csv_column.append(self.label_list_column.get(list_get[i]).strip())
            else:
                csv_column.append(self.label_list_column.get(list_get[i]))
        save_df = read_df.loc[:,csv_column]
        save_df.to_csv(f'{base_dir}/output{now.strftime("%Y%m%d-%H%M%S")}.csv', header=True,index=False)
        
        # 終了
        quit()
    
    def close(self, event):
        # 閉じる
        quit()
        
if __name__ == "__main__":
    main()
