import jingju_singing_analysis as jSA
import JMSC_plots as jplot
import pandas as pd
import os
from music21 import *
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


def get_interval_hist_single(
    linesData,
    hd=['laosheng', 'dan', 'laodan'],
    sq=['erhuang', 'xipi', 'nanbangzi', 'sipingdiao'],  # Careful with defaults
    bs=['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
        'yuanban', 'erliu', "kuai'erliu", 'liushui', 'kuaiban'],
    ju=['s', 's1', 's2', 'x'],
    countGraceNotes=True,
    ignoreGraceNotes=False,
    directedInterval=True,
    count='sum',
    silence2ignore=0.25
):
    material = jSA.collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                       banshi=bs, judou=ju)

    if material == 42:
        return

    print('\nComputing interval histogram...\nProcessing scores:')

    intervalCount = {}

    df = pd.DataFrame(columns=['P-11', 'm-10', 'P-8', 'm-7', 'M-6', 'm-6', 'P-5', 'A-4', 'd-5', 'P-4', 'M-3',
                      'm-3', 'M-2', 'm-2', 'P1', 'm2', 'M2', 'm3', 'A2', 'M3', 'P4', 'P5', 'm6', 'M6', 'm7', 'P8', 'M9', 'm10'])

    for score in tqdm(material[1:]):
        # Loading the score to get the parts list
        scorePath = score[0].split('/')
        scoreName = scorePath[-1]
        scorePath = os.path.join(*(scorePath[:-1]), 'MusicXML', scoreName)
        if not os.path.exists(scorePath):
            pre, ext = os.path.splitext(scorePath)
            scorePath = pre + '.musicxml'

        if scoreName == 'lsxp-WoZhuYe-ZhuiHanXin.xml' or scoreName == 'daeh-WeiKaiYan-DouEYuan.musicxml':
            continue  # lol k

        loadedScore = converter.parse(scorePath)
        # print('\tParsing ' + scoreName)
        parts = jSA.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0:
                continue  # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                line_number = startEnd[2]
                df.loc[line_number] = [0] * len(df.columns)
                segment = notes.getElementsByOffset(start, end)

                # Count intervals in the current segment
                # Find the last note that is not a grace note

                i = 1
                lastn = segment[-i]
                while lastn.quarterLength == 0:
                    i += 1
                    lastn = segment[-i]

                for j in range(len(segment)-i):
                    n1 = segment[j]
                    if n1.isRest:
                        continue
                    if ignoreGraceNotes:
                        if n1.quarterLength == 0:
                            continue
                    k = 1
                    while True:
                        n2 = segment[j+k]
                        if n2.isRest:
                            if n2.quarterLength <= silence2ignore:
                                k += 1
                            else:
                                n2 = None
                                break
                        elif (n2.quarterLength == 0) and (ignoreGraceNotes == True):
                            j += 1
                        else:
                            break
                    if n2 == None:
                        continue
                    intvl = interval.Interval(n1, n2)
                    if directedInterval:
                        intvlName = intvl.directedName
                    else:
                        intvlName = intvl.name
                    df.at[line_number, intvlName] += 1

    df.to_csv(f'ihd_{bs[0]}.csv')


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

    if material == 42:
        return

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

    df.to_csv(f'pitch_{bs[0]}.csv')


def get_melodic_density(
    linesData,
    hd=['laosheng', 'dan', 'laodan'],
    sq=['erhuang', 'xipi', 'nanbangzi', 'sipingdiao'],
    bs=['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
        'yuanban', 'erliu', "kuai'erliu", 'liushui', 'kuaiban'],
    ju=['s', 's1', 's2', 'x'],
    filename=None,
    includeGraceNotes=True,
    notesOrDuration='notes'
):
    material = jSA.collectLineMaterial(linesData, hangdang=hd, shengqiang=sq,
                                       banshi=bs, judou=ju)

    if material == 42:
        return

    while notesOrDuration not in ['notes', 'Notes', 'duration', 'Duration']:
        message = '\nERROR: The value given for the notesOrDuration parameter'\
            ' is invalid. Please enter either "notes" or "duration" (to'\
            ' quit the program, please type "stop"): '
        ans = input(message)
        if ans == 'stop':
            exit()
        else:
            notesOrDuration = ans

    syllables = []
    totalCount = []
    scores = []
    results = {}

    print('\nComputing melodic density...\nProcessing scores:')

    df = pd.DataFrame(columns=['median', 'Q1', 'Q3',
                      'lower fence', 'upper fence', 'outliers'])

    xLabels = []
    for score in tqdm(material[1:]):
        # Loading the score to get the parts list
        scorePath = score[0].split('/')
        scoreName = scorePath[-1]
        scorePath = os.path.join(*(scorePath[:-1]), 'MusicXML', scoreName)
        if not os.path.exists(scorePath):
            pre, ext = os.path.splitext(scorePath)
            scorePath = pre + '.musicxml'
        scores.append(scorePath)
        loadedScore = converter.parse(scorePath)
        # print('\tParsing ' + scoreName)
        localCount = []
        parts = jSA.findVoiceParts(loadedScore)
        # Work with each part
        for partIndex in range(1, len(score)):
            if len(score[partIndex]) == 0:
                continue  # Skip part if it's empty
            # Get the notes from the current part
            part = parts[partIndex-1]
            notes = part.flat.notesAndRests.stream()
            # Find segments to analyze in the current part
            for startEnd in score[partIndex]:
                start = startEnd[0]
                end = startEnd[1]
                line_number = startEnd[2]
                xLabels.append(line_number)
                segment = notes.getElementsByOffset(start, end)
                openParenthesis = False
                graceNote = False
                for i in range(len(segment)):
                    n = segment[i]
                    if notesOrDuration == 'notes':
                        value = 1
                    else:
                        value = n.quarterLength
                    if n.isRest:
                        continue
                    if n.quarterLength == 0:
                        if not includeGraceNotes:
                            continue
                        j = 1
                        while (i+j < len(segment) and
                               segment[i+j].quarterLength == 0):
                            j += 1
                        if i+j == len(segment):
                            continue
                        n2 = segment[i+j]
                        if len(n2.lyrics) > 0:
                            if (('（' in n2.lyric) or ('）' in n2.lyric) or
                                    openParenthesis):
                                localCount[-1] += value
                            else:
                                if graceNote:
                                    localCount[-1] += value
                                else:
                                    localCount.append(value)
                                    syllables.append(n2.lyric)
                                    graceNote = True
                        else:
                            localCount[-1] += value
                    else:
                        if len(n.lyrics) > 0:
                            # Check if the lyric is a padding syllable
                            if ('（' in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                            elif ('（' in n.lyric) and ('）' not in n.lyric):
                                localCount[-1] += value
                                openParenthesis = True
                            elif ('（' not in n.lyric) and ('）' in n.lyric):
                                localCount[-1] += value
                                openParenthesis = False
                            else:
                                if openParenthesis:
                                    localCount[-1] += value
                                elif graceNote:
                                    localCount[-1] += value
                                    graceNote = False
                                else:
                                    localCount.append(value)
                                    syllables.append(n.lyric)
                        else:
                            localCount[-1] += value
        totalCount.append(localCount)

    print('Melodic density computed.')

    for i in range(len(xLabels)):
        results[xLabels[i]] = {}
        results[xLabels[i]]['score'] = scores[i]

    plt.figure()
    data = plt.boxplot(totalCount)

    # Collect all statistical information in the results dictionary
    limits = []
    for i in range(len(data['medians'])):
        limits.append(np.mean(data['medians'][i].get_xdata()))
        bp = results[xLabels[i]]  # bp: boxplot
        bp['median'] = data['medians'][i].get_ydata()[0]
        bp['Q1'] = data['boxes'][i].get_ydata()[1]
        bp['Q3'] = data['boxes'][i].get_ydata()[2]
        bp['lower fence'] = data['caps'][i*2].get_ydata()[1]
        bp['upper fence'] = data['caps'][i*2+1].get_ydata()[1]
        bp['outliers'] = data['fliers'][i].get_ydata().tolist()

    keys = ['median', 'Q1', 'Q3', 'lower fence', 'upper fence']
    for i in range(len(results)):
        line_number = xLabels[i]
        x = results[line_number]
        df.loc[line_number] = [0] * len(df.columns)
        for k in keys:
            df.at[line_number, k] += x[k]
        df.at[line_number, 'outliers'] = len(x['outliers'])

    filename = 'melodic_density_'
    if notesOrDuration == 'duration':
        filename += 'duration_'
    elif notesOrDuration == 'notes':
        filename += 'notes_'
    filename += bs[0] + '.csv'
    df.to_csv(filename)


if __name__ == "__main__":
    hd_all = ['laosheng', 'dan', 'laodan']
    sq_all = ['erhuang', 'xipi', 'nanbangzi', 'sipingdiao']
    bs_all = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
              'yuanban', 'erliu', "kuai'erliu", 'liushui', 'kuaiban']
    linesData = '../../Jingju Scores Dataset/fixed.csv'

    for bs in bs_all:
        get_pitch_hist_single(linesData, bs=[bs])
        get_interval_hist_single(linesData, bs=[bs])
        get_melodic_density(linesData, bs=[bs])  # Notes
        get_melodic_density(
            linesData, bs=[bs], notesOrDuration='duration')  # Duration
