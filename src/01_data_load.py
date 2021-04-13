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
    data.drop(data.index[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], inplace=True)

    # droping unecessary columnd
    data.drop(data.columns[[5, 6, 7, 8, 9, 10]], axis=1, inplace=True)

    # renaming columns
    data.columns = ['woj', 'pow', 'pow_name', 'unempl_no', 'unempl_%']

    # droping rows with voivodship name
    data = data[data['pow'] != '00']

    # reseting index
    data.reset_index(inplace=True, drop=True)

    # creating teryt column
    data['teryt'] = data.apply(lambda x: str(x['woj']) + str(x['pow']), axis=1)

    # getting rid of spaces
    data['pow_name'] = data['pow_name'].apply(lambda x: str(x).replace(' ', ''))

    data['pow_name'] = data['pow_name'].apply(lambda x: str(x).replace('m.', 'miasto ') if str(x).find('m.') != -1 else "powiat " + str(x))

    print(data.head(10))
    data_save_path = r'\data\interim\unemployment.xlsx'
    data.to_excel(project_dir + data_save_path, index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')


if __name__ == "__main__":
    main()