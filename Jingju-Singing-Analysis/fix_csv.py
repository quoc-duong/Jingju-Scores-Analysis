import pandas as pd
import numpy as np
import os


def main():
    hd_all = ['laosheng', 'dan', 'laodan']
    sq_all = ['erhuang', 'xipi']
    bs_all = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
              'yuanban', 'erliu', 'liushui', 'kuaiban']
    mel_den_dur = 'melodic_density_duration_'
    mel_den_notes = 'melodic_density_notes_'
    for bs in bs_all:
        filename_dur = mel_den_dur + bs + '.csv'
        filename_notes = mel_den_notes + bs + '.csv'

        df_duration = pd.read_csv(filename_dur, index_col=0)
        df_notes = pd.read_csv(filename_notes, index_col=0)
        df_duration = df_duration.iloc[:, [0]]
        df_notes = df_notes.iloc[:, [0]]

        df_duration = df_duration.rename(columns={"median": "median_duration"})
        df_notes = df_notes.rename(columns={"median": "median_notes"})

        df_duration.to_csv(filename_dur, index=True)
        df_notes.to_csv(filename_notes, index=True)


if __name__ == '__main__':
    main()
