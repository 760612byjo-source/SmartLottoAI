import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data")


def get_excel_files():

    files = []

    for file in DATA_FOLDER.glob("*.*"):

        if file.suffix.lower() in [".xlsx", ".xlsm"]:
            files.append(file.name)

    return files


def get_sheet_names(file_name):

    file_path = DATA_FOLDER / file_name

    xls = pd.ExcelFile(file_path)

    return xls.sheet_names


def load_sheet(file_name, sheet_name):

    file_path = DATA_FOLDER / file_name

    try:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=None
        )

        return df

    except Exception as e:

        return str(e)