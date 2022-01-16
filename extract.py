#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, os, pandas, json, re


def main():
    read_df = pandas.read_csv("Data/dummy.csv", encoding='utf-8')  # CSV読み込み
    json_open = open(file="Data/format.json", mode='r', encoding='utf-8')  # フォーマット読み込み
    json_load = json.load(json_open)
    add_column = json_load["Save-column"]
    format_json = json_load["Transfer-column"]
    out_df = read_df.loc[:, add_column]

    for i in range(len(add_column)):
        # 指定文字内抜き出し
        if "extract" in format_json[i][add_column[i]]:
            for j in range(len(out_df)):
                out_df[add_column[i]][j] = \
                    re.findall(f"{format_json[i][add_column[i]]['extract'][0]}(.*){format_json[i][add_column[i]]['extract'][1]}", out_df[add_column[i]][j])[0]

        # 指定文字以前抜き出し
        if "extract-before" in format_json[i][add_column[i]]:
            for j in range(len(out_df)):
                out_df[add_column[i]][j] = \
                    re.findall(f"(.*){format_json[i][add_column[i]]['extract-before']}", out_df[add_column[i]][j])[0]

        # 指定文字以降抜き出し
        if "extract-after" in format_json[i][add_column[i]]:
            for j in range(len(out_df)):
                out_df[add_column[i]][j] = \
                    re.findall(f"{format_json[i][add_column[i]]['extract-after']}(.*)", out_df[add_column[i]][j])[0]

    print(out_df)


if __name__ == '__main__':
    main()