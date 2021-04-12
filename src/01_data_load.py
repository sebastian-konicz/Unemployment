from pathlib import Path
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading data
    # gettig the file with PNA data
    data_path = r'\data\raw\stopa_bezrobocia_za_luty_2021.xlsx'
    data = pd.read_excel(project_dir + data_path, sheet_name='Tabl.1a', header=None)

    # cleaning loaded data to dataframe format
    # droping unecessary rows
    data.drop([data.index[0], data.index[1], data.index[2], data.index[3], data.index[4],
               data.index[5], data.index[6], data.index[7], data.index[8], data.index[9]], inplace=True)

    # droping unecessary columnd
    data.drop(data.columns[[5, 6, 7, 8, 9, 10]], axis=1, inplace=True)

    # renaming columns
    data.columns = ['woj', 'pow', 'pow_name', 'unempl_no', 'unempl_%']

    # droping rows with voivodship name
    data = data[data['pow'] != '00']

    # reseting index
    data.reset_index(inplace=True, drop=True)

    print(data.head(10))


    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')


if __name__ == "__main__":
    main()