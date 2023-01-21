# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 18:52:06 2023

@author: kujoh
"""

import numpy as np
from collections import defaultdict
from matplotlib.patches import Patch

def bar_plot(ax, data, group_stretch=0.8, bar_stretch=0.95,
             legend=True, x_labels=True, label_fontsize=8,
             colors=None, barlabel_offset=1,
             bar_labeler=lambda k, i, s: str(round(s, 3)), 
             bar_labeler_text='', barlbl_add=''):
    """
    Draws a bar plot with multiple bars per data point.
    
    :param dict data: The data we want to plot, wher keys are the names of each
      bar group, and items is a list of bar values for the corresponding group.
      
    :param float group_stretch: 1 means groups occupy the most (largest groups
      touch side to side if they have equal number of bars).
    
    :param float bar_stretch: If 1, bars within a group will touch side to side.
    
    :param bool x_labels: If true, x-axis will contain labels with the group
      names given at data, centered at the bar group.
      
    :param int label_fontsize: Font size for the label on top of each bar.
    
    :param float barlabel_offset: Distance, in y-values, between the top of the
      bar and its label.
      
    :param function bar_labeler: If not None, must be a functor with signature
      ``f(group_name, i, scalar)->str``, where each scalar is the entry found at
      data[group_name][i]. When given, returns a label to put on the top of each
      bar. Otherwise no labels on top of bars.
    """
    sorted_data = list(sorted(data.items(), key=lambda elt: elt[0]))
    sorted_k, sorted_v  = zip(*sorted_data)
    max_n_bars = max(len(v) for v in data.values())
    group_centers = np.cumsum([max_n_bars
                               for _ in sorted_data]) - (max_n_bars / 2)
    bar_offset = (1 - bar_stretch) / 2
    bars = defaultdict(list)
    #
    if colors is None:
        colors = {g_name: [f"C{i}" for _ in values]
                  for i, (g_name, values) in enumerate(data.items())}
    #
    for g_i, ((g_name, vals), g_center) in enumerate(zip(sorted_data,
                                                         group_centers)):
        n_bars = len(vals)
        group_beg = g_center - (n_bars / 2) + (bar_stretch / 2)
        for val_i, val in enumerate(vals):
            try:
                bar = ax.bar(group_beg + val_i + bar_offset,
                             height=val, width=bar_stretch,
                             color=colors[g_name][val_i])[0]
            except KeyError:
                bar = ax.bar(group_beg + val_i + bar_offset,
                             height=val, width=bar_stretch,
                             color=colors[g_name][val_i-2])[0]
            
            bars[g_name].append(bar)
            if  bar_labeler is not None:
                l_pos = bar.get_x() + bar.get_height()/2.
                
                x_pos = bar.get_x() + (bar.get_width() / 2.0)
                y_pos = val + barlabel_offset
                barlbl = bar_labeler(g_name, val_i, val)
                ax.text(x_pos, y_pos, barlbl+barlbl_add, ha="center", va="bottom",
                        fontsize=label_fontsize)
                ax.text(x_pos, l_pos, bar_labeler_text[val_i], ha="center", color="white")
    if legend:
        handles = []
        labels = []
        
        for i in [0, 1]:
            for j, k in enumerate(sorted_k):
                handles.append(Patch(facecolor=colors[k][i], edgecolor='black'))
                labels.append('')
        
        for i, k in enumerate(reversed(list(sorted_k))):
            labels[i] = k    
        labels.reverse()
                
        ax.legend(handles=handles,
                  labels=labels,
                  ncol=2, handletextpad=0.5, handlelength=1.0, columnspacing=-0.5,
                  loc='best', framealpha=1,
                  edgecolor='k').get_frame().set_boxstyle('square')
    #
    ax.set_xticks(group_centers)
    if x_labels:
        ax.set_xticklabels(sorted_k)
    else:
        ax.set_xticklabels()
    return bars, group_centers