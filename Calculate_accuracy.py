import pandas as pd
from sklearn.metrics import classification_report
import os
import base64

# Input the paths for both images and texts:
code_book_path = "Code Book.xlsx"
df = pd.read_excel(code_book_path)
results = pd.read_csv("emotion_analysis_results_with_all_LLMs.csv")

Y = df["label"]
Y_gpt = results["chatgpt_classification"]
Y_grok = results["grok_classification"]
Y_deepseek = results["deepseek_classification"]
Y_idx = df["adult"]

report1 = classification_report(Y, Y_gpt, output_dict=True)
report2 = classification_report(Y, Y_grok, output_dict=True)
report3 = classification_report(Y, Y_deepseek, output_dict=True)

# separate
report1_adult = classification_report(Y[Y_idx == 1], Y_gpt[Y_idx == 1], output_dict=True)
report2_adult = classification_report(Y[Y_idx == 1], Y_grok[Y_idx == 1], output_dict=True)
report3_adult = classification_report(Y[Y_idx == 1], Y_deepseek[Y_idx == 1], output_dict=True)

report1_child = classification_report(Y[Y_idx == 0], Y_gpt[Y_idx == 0], output_dict=True)
report2_child = classification_report(Y[Y_idx == 0], Y_grok[Y_idx == 0], output_dict=True)
report3_child = classification_report(Y[Y_idx == 0], Y_deepseek[Y_idx == 0], output_dict=True)