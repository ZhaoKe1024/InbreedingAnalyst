#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 17:47
# @Author: ZhaoKe
# @File : myself.py
# @Software: PyCharm

from inbreed_lib.BreedingMainESR import run_main_with_graph


if __name__ == '__main__':
    # run_main_without_graph(file_path="./analyzer/kinship330.csv", result_file="./analyzer/output_{}.csv")
    # run_main_with_graph(file_path="./datasets/first330.xlsx", gene_idx="2025", result_file="./temp_files/output_{}.xlsx")
    run_main_with_graph(file_path="./temp_files/output_2025.xlsx", gene_idx="2026", result_file="./temp_files/output_{}.xlsx")
