import jingju_singing_analysis as jSA
import JMSC_plots as jplot
import pandas as pd
import os
from music21 import *
from tqdm import tqdm


def get_pitch_hist_single(
    linesData,
    hd=['laosheng', 'dan', 'laodan'],
    sq=['erhuang', 'xipi', 'nanbangzi', 'sipingdiao'],  # Careful with defaults
    bs=['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
        'yuanban', 'erliu', "kuai'erliu", 'liushui', 'kuaiban'],
    ju=['s', 's1', 's2', 'x'],
    countGraceNotes=True
):
    # get all info from laosheng stuff with collectLineMaterial
    material = jSA.collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                       banshi=bs, judou=ju)

    df = pd.DataFrame(columns=['F#3', 'G#3', 'A3', 'A#3', 'B3', 'C#4',
                      'C##4', 'D#4', 'E4', 'F#4', 'G#4', 'A4', 'A#4', 'B4', 'C#5', 'D#5', 'E5', 'F#5', 'G#5', 'A5', 'A#5', 'B5', 'C#6'])

    for score in tqdm(material[1:]):
        scorePath = score[0].split('/')
        scoreName = scorePath[-1]
        scorePath = os.path.join(*(scorePath[:-1]), 'MusicXML', scoreName)
        if not os.path.exists(scorePath):
            pre, ext = os.path.splitext(scorePath)
            scorePath = pre + '.musicxml'
        loadedScore = converter.parse(scorePath)

        parts = jSA.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0:
                continue  # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notes.stream()

            # Set the duration of grace notes if needed
            if countGraceNotes:
                minDur = 0.25
                for n in notes:
                    noteDur = n.quarterLength
                    if noteDur != 0 and noteDur < minDur:
                        minDur = noteDur

            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                line_number = startEnd[2]
                segment = notes.getElementsByOffset(start, end)
                df.loc[line_number] = [0] * len(df.columns)
                # Count pitches in the current segment
                for n in segment:
                    noteName = n.nameWithOctave
                    noteDur = n.quarterLength
                    if noteDur == 0:
                        if not countGraceNotes:
                            continue
                    df.at[line_number, noteName] += noteDur

    df.to_csv(f'pitch_{hd[0]}.csv')


if __name__ == "__main__":
    get_pitch_hist_single(
        linesData='../../Jingju Scores Dataset/fixed.csv', hd=['laosheng'])

    get_pitch_hist_single(
        linesData='../../Jingju Scores Dataset/fixed.csv', hd=['laodan'])

    get_pitch_hist_single(
        linesData='../../Jingju Scores Dataset/fixed.csv', hd=['dan'])
