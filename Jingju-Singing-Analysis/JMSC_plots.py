# -*- coding: utf-8 -*-


# JMSC_plots.py is a script for reproducing with a single command line all the
# plots and tables computed from the Jingju Music Scores Collection
# (http://doi.org/10.5281/zenodo.1464653) and used in the following
# publication:
#   Caro Repetto, Rafael (2018) *The musical dimension of Chinese traditional
#   theatre: An analysis from computer aided musicology*. PhD thesis,
#   Universitat Pompeu Fabra, Barcelona, Spain.
#
# Copyright (C) 2018 Music Technology Group, Universitat Pompeu Fabra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import jingju_singing_analysis as jSA
import argparse
import time

# General variables

# Roles
role_all = ['laosheng', 'dan', 'laodan']

# Shengqiang
shengqiang_all = ['erhuang', 'xipi', 'nanbangzi', 'sipingdiao']

# Banshi grouped with different metres
banshi_2_4 = ['yuanban', 'erliu', "kuai'erliu"]
banshi_4_4 = ['manban', 'sanyan', 'zhongsanyan', 'kuaisanyan']
banshi_1_4 = ['kuaiban', 'liushui']
bs = ['yuanban', 'erliu', "kuai'erliu", 'manban', 'sanyan', 'zhongsanyan', 'kuaisanyan',
      'kuaiban', 'liushui']

# Line types
ju = ['s', 's1', 's2', 'x']

# Define lists
figs = ['ph', 'ihd', 'mdn', 'mdd']

# Pitch histogram
ph = [['ph-laosheng.png', [role_all[0]], shengqiang_all, bs, ju],
      ['ph-dan.png', [role_all[1]], shengqiang_all, bs, ju],
      ['ph-laodan.png', [role_all[2]], shengqiang_all, bs, ju]]

# Directed interval histogram
ihd = [['ihd-laosheng.png', [role_all[0]], shengqiang_all, bs, ju],
       ['ihd-dan.png', [role_all[1]], shengqiang_all, bs, ju],
       ['ihd-laodan.png', [role_all[2]], shengqiang_all, bs, ju]]

# cn = [['cn-ls-eh.png', ls, eh, bs],
#      ['cn-da-xp-kb.png', da, xp, kb]]

# Melody density by notes
mdn = [['mdn-laosheng.png', [role_all[0]], shengqiang_all, bs, ju],
       ['mdn-dan.png', [role_all[1]], shengqiang_all, bs, ju],
       ['mdn-laodan.png', [role_all[2]], shengqiang_all, bs, ju]]

# Melody density by duration
mdd = [['mdd-laosheng.png', [role_all[0]], shengqiang_all, bs, ju],
       ['mdd-dan.png', [role_all[1]], shengqiang_all, bs, ju],
       ['mdd-laodan.png', [role_all[2]], shengqiang_all, bs, ju]]

# Define plotting functions


def plot_ph(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting pitch histograms                                       '
          '           ##')
    print('##################################################################'
          '#############')

    to_print = ''

    ph_folder = 'pitch_histograms'
    folder = root_folder + '/' + ph_folder
    if ph_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the pitch '
              'histogram figures.')
        os.mkdir(folder)
    else:
        print('\nPitch histogram figures will be saved in the existing folder'
              ' ' + folder + '.')

    for phi in ph:
        print('\nComputing figure "' + phi[0] + '"')
        fn = folder + '/' + phi[0]
        to_print += phi[0] + '\n'
        ph_results = jSA.pitchHistogram(linesData, hd=phi[1], sq=phi[2],
                                        bs=phi[3], ju=phi[4], filename=fn)
        for line in ph_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/ph_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_phlj(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting pitch histograms for sections in line                  '
          '           ##')
    print('##################################################################'
          '#############')

    to_print = ''

    phlj_folder = 'pitch_histograms_sections'
    folder = root_folder + '/' + phlj_folder
    if phlj_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the pitch '
              'histogram figures.')
        os.mkdir(folder)
    else:
        print('\nPitch histogram figures will be saved in the existing folder'
              ' ' + folder + '.')

    for phlji in phlj:
        print('\nComputing figure "' + phlji[0] + '"')
        fn = folder + '/' + phlji[0]
        to_print += phlji[0] + '\n'
        phlj_results = jSA.pitchHistogramLineJudou(linesData, hd=phlji[1],
                                                   sq=phlji[2], bs=phlji[3],
                                                   ju=phlji[4], filename=fn)
        for row in range(len(phlj_results[0])):
            to_print += phlj_results[0][row][0] + ',' +\
                str(phlj_results[0][row][1]) + ',' +\
                str(phlj_results[1][row][1]) + ',' +\
                str(phlj_results[2][row][1]) + '\n'
        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/phlj_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_ihd(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting histograms of directed intervals                       '
          '           ##')
    print('##################################################################'
          '#############')

    to_print = ''

    ihd_folder = 'directed_interval_histograms'
    folder = root_folder + '/' + ihd_folder
    if ihd_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the interval'
              ' histogram figures.')
        os.mkdir(folder)
    else:
        print('\nInterval histogram figures will be saved in the existing '
              'folder ' + folder + '.')

    for ihdi in ihd:
        print('\nComputing figure "' + ihdi[0] + '"')
        fn = folder + '/' + ihdi[0]
        to_print += ihdi[0] + '\n'
        ihd_results = jSA.intervalHistogram(linesData, hd=ihdi[1], sq=ihdi[2],
                                            bs=ihdi[3], ju=ihdi[4],
                                            filename=fn, directedInterval=True)
        for line in ihd_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/ihd_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_ihn(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting histograms of not directed intervals                   '
          '           ##')
    print('##################################################################'
          '#############')

    to_print = ''

    ihn_folder = 'non_directed_interval_histograms'
    folder = root_folder + '/' + ihn_folder
    if ihn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the interval'
              ' histogram figures.')
        os.mkdir(folder)
    else:
        print('\nInterval histogram figures will be saved in the existing '
              'folder ' + folder + '.')

    for ihni in ihn:
        print('\nComputing figure "' + ihni[0] + '"')
        fn = folder + '/' + ihni[0]
        to_print += ihni[0] + '\n'
        ihn_results = jSA.intervalHistogram(linesData, hd=ihni[1], sq=ihni[2],
                                            bs=ihni[3], ju=ihni[4],
                                            filename=fn,
                                            directedInterval=False)
        for line in ihn_results:
            to_print += line[0] + ',' + str(line[1]) + '\n'
        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/ihn_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_cn(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting cadential notes                                        '
          '           ##')
    print('##################################################################'
          '#############')

    to_print = ''

    cn_folder = 'cadential_notes'
    folder = root_folder + '/' + cn_folder
    if cn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the '
              'cadential notes figures.')
        os.mkdir(folder)
    else:
        print('\nCadential notes figures will be saved in the existing folder'
              ' ' + folder + '.')

    for cni in cn:
        print('\nComputing figure "' + cni[0] + '"')
        fn = folder + '/' + cni[0]
        to_print += cni[0] + '\n'
        cn_results = jSA.cadentialNotes(linesData, hd=cni[1], sq=cni[2],
                                        bs=cni[3], filename=fn)
        if len(cn_results) == 2:
            to_print += ',Op. line,,,Cl. line,,\n,S1,S2,S3,S1,S2,S3\n'
            ol = cn_results['Op. line']
            cl = cn_results['Cl. line']
            for row in range(len(ol['S1'])):
                to_print += ol['S1'][row][0] + ',' +\
                    str(ol['S1'][row][1]) + ',' +\
                    str(ol['S2'][row][1]) + ',' +\
                    str(ol['S3'][row][1]) + ',' +\
                    str(cl['S1'][row][1]) + ',' +\
                    str(cl['S2'][row][1]) + ',' +\
                    str(cl['S3'][row][1]) + '\n'
        elif len(cn_results) == 3:
            to_print += ',Op. l. 1,,,Op. l. 2,,,Cl. line,,\n,S1,S2,S3,S1,S2,S3,S1,S2,S3\n'
            ol1 = cn_results['Op. l. 1']
            ol2 = cn_results['Op. l. 2']
            cl = cn_results['Cl. l.']
            for row in range(len(ol1['S1'])):
                to_print += ol1['S1'][row][0] + ',' +\
                    str(ol1['S1'][row][1]) + ',' +\
                    str(ol1['S2'][row][1]) + ',' +\
                    str(ol1['S3'][row][1]) + ',' +\
                    str(ol2['S1'][row][1]) + ',' +\
                    str(ol2['S2'][row][1]) + ',' +\
                    str(ol2['S3'][row][1]) + ',' +\
                    str(cl['S1'][row][1]) + ',' +\
                    str(cl['S2'][row][1]) + ',' +\
                    str(cl['S3'][row][1]) + '\n'
        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/cn_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_mdn(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting melodic density as notes                               '
          '           ##')
    print('##################################################################'
          '#############')

    keys = ['median', 'Q1', 'Q3', 'lower fence', 'upper fence']

    to_print = ''

    mdn_folder = 'melodic_density_notes'
    folder = root_folder + '/' + mdn_folder
    if mdn_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the melodic '
              'density figures.')
        os.mkdir(folder)
    else:
        print('\nMelodic density figures will be saved in the existing folder'
              ' ' + folder + '.')

    for mdni in mdn:
        print('\nComputing figure "' + mdni[0] + '"')
        fn = folder + '/' + mdni[0]
        to_print += mdni[0] + '\n'
        mdn_results = jSA.melodicDensity(linesData, hd=mdni[1], sq=mdni[2],
                                         bs=mdni[3], ju=mdni[4], filename=fn,
                                         notesOrDuration='notes')

        to_print += 'index,score,median,Q1,Q3,lower fence,upper fence,'\
                    'outliers\n'
        for i in range(1, len(mdn_results)):
            x = mdn_results[str(i)]
            to_print += str(i) + ',' + x['score'].split('/')[-1] + ','
            for k in keys:
                to_print += str(x[k]) + ','
            for o in x['outliers']:
                to_print += str(o) + ';'
            to_print = to_print[:-1] + '\n'

        to_print += 'Avg' + ',,'
        avg = mdn_results['Avg']
        for k in keys:
            to_print += str(avg[k]) + ','
        for o in avg['outliers']:
            to_print += str(o) + ';'
        to_print = to_print[:-1] + '\n'

        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/mdn_results.csv', 'w') as f:
        f.write(to_print[:-1])


def plot_mdd(linesData, root_folder):
    print('\n\n##############################################################'
          '#################')
    print('## Ploting melodic density as quarter length duration             '
          '           ##')
    print('##################################################################'
          '#############')

    keys = ['median', 'Q1', 'Q3', 'lower fence', 'upper fence']

    to_print = ''

    mdd_folder = 'melodic_density_duration'
    folder = root_folder + '/' + mdd_folder
    if mdd_folder not in os.listdir(root_folder):
        print('\nThe "' + folder + '" folder was created to save the melodic '
              'density figures.')
        os.mkdir(folder)
    else:
        print('\nMelodic density figures will be saved in the existing folder'
              ' ' + folder + '.')

    for mddi in mdd:
        print('\nComputing figure "' + mddi[0] + '"')
        fn = folder + '/' + mddi[0]
        to_print += mddi[0] + '\n'
        mdd_results = jSA.melodicDensity(linesData, hd=mddi[1], sq=mddi[2],
                                         bs=mddi[3], ju=mddi[4], filename=fn,
                                         notesOrDuration='duration')

        to_print += 'index,score,median,Q1,Q3,lower fence,upper fence,'\
                    'outliers\n'
        for i in range(1, len(mdd_results)):
            x = mdd_results[str(i)]
            to_print += str(i) + ',' + x['score'].split('/')[-1] + ','
            for k in keys:
                to_print += str(x[k]) + ','
            for o in x['outliers']:
                to_print += str(o) + ';'
            to_print = to_print[:-1] + '\n'

        to_print += 'Avg' + ',,'
        avg = mdd_results['Avg']
        for k in keys:
            to_print += str(avg[k]) + ','
        for o in avg['outliers']:
            to_print += str(o) + ';'
        to_print = to_print[:-1] + '\n'

        print('\n____________________________________________________________'
              '___________________')

    with open(folder + '/mdd_results.csv', 'w') as f:
        f.write(to_print[:-1])


###############################################################################
## PLOTTING                                                                  ##
###############################################################################
if __name__ == '__main__':

    time0 = time.time()

    parser = argparse.ArgumentParser(description='Compute seven different '
                                                 'types of statistical '
                                                 'information from the Jingju'
                                                 ' Music Scores Collections '
                                                 'according to different line'
                                                 ' categories. For each type,'
                                                 ' return a csv file with '
                                                 'numerical information and a'
                                                 ' series of related plots.')
    parser.add_argument('linesData', help='Path to the lines_data.csv file, '
                                          'which should be stored in the same'
                                          ' folder as the MusicXML scores of '
                                          'the Jingju Music Scores Collection')
    parser.add_argument('-f', '--figures', nargs='*',
                        choices=figs,
                        help='Select which information type to compute:  ph '
                             '-- pitch histograms per line; phlj -- pitch '
                             'histograms per line sections; ihn -- non '
                             'directed interval histograms; ihd -- directed'
                             ' interval histograms; cn -- cadential notes; '
                             'mdn -- melodic density as notes; mdd -- melodic'
                             ' density as duration. If no argument is passed,'
                             ' information for all seven types is computed.')
    parser.add_argument('-p', '--path', help='Path to the location where the '
                                             '"plots" folder containing all '
                                             'the returned files will be '
                                             'saved')

    args = parser.parse_args()

    # Create a folder for storing the plots
    if args.path == None:
        p = '.'
    else:
        if args.path[-1] == '/':
            p = args.path[:-1]
        else:
            p = args.path

    root_folder = p + '/plots'

    if 'plots' not in os.listdir(p):
        print('\nThe folder "' + root_folder + '" was created to save the '
              'figures.')
        os.mkdir(root_folder)
    else:
        print('\nThe figures will be saved in the existing folder "' +
              root_folder + '".')

    # Define the list of figures to plot
    if args.figures == None:
        to_plot = figs
    else:
        to_plot = args.figures

    # Plot figures
    if 'ph' in to_plot:
        plot_ph(args.linesData, root_folder)

    if 'ihd' in to_plot:
        plot_ihd(args.linesData, root_folder)

#    if 'cn' in to_plot:
#        plot_cn(args.linesData, root_folder)

    if 'mdn' in to_plot:
        plot_mdn(args.linesData, root_folder)

    if 'mdd' in to_plot:
        plot_mdd(args.linesData, root_folder)

    # Confirmation message
    print('\n================================================================'
          '===============')
    print('--- FINISHED! ---')
    print('All the figures plotted and saved correctly.')
    print('(Required time: ' + time.strftime('%H:%M\'%S")',
                                             time.gmtime(time.time()-time0)))
    print('=================================================================='
          '=============')
