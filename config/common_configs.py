import os
import pathlib


base_dir = pathlib.Path(__file__).parent.absolute().parent

data_dir = os.path.join(base_dir, "src", "data")
prompt_dir = os.path.join(base_dir, "src", "prompt")


options = {}

options["investors_data_csv"] = os.path.join(data_dir, "top_investors_cleaned.csv")
options["system_prompt_file"] = os.path.join(prompt_dir, "system_prompt.txt")