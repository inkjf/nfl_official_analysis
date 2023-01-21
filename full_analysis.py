# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 08:24:43 2023

@author: john.ink
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from custom_barplot import bar_plot
from nfl_teams import Teams

from statistics import mean, StatisticsError


team_abbrev = {'all' : 'all',
               'Kansas City Chiefs' : 'kcc',
               'Denver Broncos' : 'den',
               'Los Angeles Chargers' : 'lac',
               'Las Vegas Raiders' : 'lvr',
               'New England Patriots' : 'pats'
               }


parameter_list = ['HomeAveragePenaltyYards', 'HomeAveragePenalties',
                  'AwayAveragePenaltyYards', 'AwayAveragePenalties']


def _sort_favorites(df: pd.DataFrame, team: str, atHome: bool, favorite: bool)->pd.DataFrame:
    # if team != 'all':
    if team == 'League':
        # Filter by home/away favorites
        if atHome:
            df = df[df.HomeTeam == df.Favorite] if favorite else df[df.HomeTeam != df.Favorite]
        elif atHome == False:
            df = df[df.AwayTeam == df.Favorite] if favorite else df[df.AwayTeam != df.Favorite]
    else:
        if atHome:
            df = df[df.HomeTeam == team]
    
            if favorite:
                df = df[df.HomeTeam == df.Favorite]
            else:
                df = df[df.HomeTeam != df.Favorite]
    
        elif atHome == False:
            df = df[df.AwayTeam == team]
    
            if favorite:
                df = df[df.AwayTeam == df.Favorite]
            else:
                df = df[df.AwayTeam != df.Favorite]
                
        else:
            # Don't care, either home/away
            df = df[(df.HomeTeam == team) | (df.AwayTeam == team)]
    
            if favorite:
                df = df[df.Favorite == team]
            else:
                df = df[df.Favorite != team]
    
    
    return df
    

def ats_ref_analysis(df: pd.DataFrame(), ref, teams='all', atHome=False, favorite=None, years='all', still_reffing=True):
    orig_df = df
    master_dict = {}

    for team in teams:
        df = orig_df
        df = df[df.Referee == ref]
        
        df = _sort_favorites(df, team=team, atHome=atHome, favorite=favorite)

        if years != 'all':
            (start, end) = years.split('-')
            df = df[(df.Year >= int(start)) & (df.Year <= int(end))]

        full_ref_df = orig_df[orig_df.Referee == ref]

        if not df.empty:
            if still_reffing:
                still_active = full_ref_df.Year.iloc[-1] >= 2022
            else:
                still_active = True

            if still_active:
                master_dict[team] = {}

                avg_home_pens = mean(df.HomeNumberOfPenalties)
                avg_away_pens = mean(df.AwayNumberOfPenalties)

                avg_home_penyards = mean(df.HomePenaltyYards)
                avg_away_penyards = mean(df.AwayPenaltyYards)

                if favorite:
                    perf_ats = mean(df.Covered)
                else:
                    perf_ats = mean(~df.Covered)

                master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
                master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
                master_dict[team]['GameCount'] = len(df)
                master_dict[team]['TmAveragePenalties'] = avg_home_pens
                master_dict[team]['TmAveragePenaltyYards'] = avg_home_penyards
                master_dict[team]['OppAveragePenalties'] = avg_away_pens
                master_dict[team]['OppAveragePenaltyYards'] = avg_away_penyards
                master_dict[team]['ATS'] = perf_ats
        else:
            master_dict[team] = {}
            master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
            master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
            master_dict[team]['GameCount'] = len(df)
            master_dict[team]['TmAveragePenalties'] = 0.
            master_dict[team]['TmAveragePenaltyYards'] = 0.
            master_dict[team]['OppAveragePenalties'] = 0.
            master_dict[team]['OppAveragePenaltyYards'] = 0.
            master_dict[team]['ATS'] = 0


    return pd.DataFrame(master_dict).T
    

def ats_indv_ref(df, ref, teams, year_range_list, atHome, favorite, still_reffing=False):
    orig_df = df
    master_dict = {}
    
    # Note: the teams list and year range have to have the same dimension
    for team, year_range in zip(teams, year_range_list):
        df = orig_df
        df = df[df.Referee == ref]
        
        df = _sort_favorites(df, team=team, atHome=atHome, favorite=favorite)

        if year_range != 'all':
            (start, end) = year_range.split('-')
            df = df[(df.Year >= int(start)) & (df.Year <= int(end))]

        full_ref_df = orig_df[orig_df.Referee == ref]

        if not df.empty:
            if still_reffing:
                still_active = full_ref_df.Year.iloc[-1] >= 2022
            else:
                still_active = True

            if still_active:
                if team in master_dict.keys():
                    team += '-1'
                master_dict[team] = {}

                avg_home_pens = mean(df.HomeNumberOfPenalties)
                avg_away_pens = mean(df.AwayNumberOfPenalties)

                avg_home_penyards = mean(df.HomePenaltyYards)
                avg_away_penyards = mean(df.AwayPenaltyYards)

                if favorite:
                    perf_ats = mean(df.Covered)
                else:
                    perf_ats = mean(~df.Covered)

                master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
                master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
                master_dict[team]['GameCount'] = len(df)
                master_dict[team]['TmAveragePenalties'] = avg_home_pens
                master_dict[team]['TmAveragePenaltyYards'] = avg_home_penyards
                master_dict[team]['OppAveragePenalties'] = avg_away_pens
                master_dict[team]['OppAveragePenaltyYards'] = avg_away_penyards
                master_dict[team]['ATS'] = perf_ats
        else:
            master_dict[team] = {}
            master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
            master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
            master_dict[team]['GameCount'] = len(df)
            master_dict[team]['TmAveragePenalties'] = 0.
            master_dict[team]['TmAveragePenaltyYards'] = 0.
            master_dict[team]['OppAveragePenalties'] = 0.
            master_dict[team]['OppAveragePenaltyYards'] = 0.
            master_dict[team]['ATS'] = 0


    return pd.DataFrame(master_dict).T


def ats_no_ref(df, teams, year_range_list, atHome, favorite):
    orig_df = df
    master_dict = {}
    
    if not year_range_list:
        [year_range_list.append('all') for t in teams]
    
    # Note: the teams list and year range have to have the same dimension
    for team, year_range in zip(teams, year_range_list):
        if team == 'League':
            master_dict[team] = {}
            df = _sort_favorites(df, team=team, atHome=atHome, favorite=favorite)
    
            avg_home_pens = mean(df.HomeNumberOfPenalties)
            avg_away_pens = mean(df.AwayNumberOfPenalties)
    
            avg_home_penyards = mean(df.HomePenaltyYards)
            avg_away_penyards = mean(df.AwayPenaltyYards)
    
            if favorite:
                perf_ats = mean(df.Covered)
            else:
                perf_ats = mean(~df.Covered)
    
            master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
            master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
            master_dict[team]['GameCount'] = len(df)
            master_dict[team]['TmAveragePenalties'] = avg_home_pens
            master_dict[team]['TmAveragePenaltyYards'] = avg_home_penyards
            master_dict[team]['OppAveragePenalties'] = avg_away_pens
            master_dict[team]['OppAveragePenaltyYards'] = avg_away_penyards
            master_dict[team]['ATS'] = perf_ats
        else:
            df = orig_df
            df = _sort_favorites(df, team=team, atHome=atHome, favorite=favorite)
    
            if year_range != 'all':
                (start, end) = year_range.split('-')
                df = df[(df.Year >= int(start)) & (df.Year <= int(end))]
            
            master_dict[team] = {}
    
            avg_home_pens = mean(df.HomeNumberOfPenalties)
            avg_away_pens = mean(df.AwayNumberOfPenalties)
    
            avg_home_penyards = mean(df.HomePenaltyYards)
            avg_away_penyards = mean(df.AwayPenaltyYards)
    
            if favorite:
                perf_ats = mean(df.Covered)
            else:
                perf_ats = mean(~df.Covered)
    
            master_dict[team]['AtHome'] = 'Yes' if atHome else 'No'
            master_dict[team]['Favorite'] = 'Yes' if favorite else 'No'
            master_dict[team]['GameCount'] = len(df)
            master_dict[team]['TmAveragePenalties'] = avg_home_pens
            master_dict[team]['TmAveragePenaltyYards'] = avg_home_penyards
            master_dict[team]['OppAveragePenalties'] = avg_away_pens
            master_dict[team]['OppAveragePenaltyYards'] = avg_away_penyards
            master_dict[team]['ATS'] = perf_ats

    return pd.DataFrame(master_dict).T


def generate_conference_comparison(data, ref_list):
    afcw_teams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Denver Broncos']    
    afce_teams = ["Buffalo Bills", "Miami Dolphins", "New York Jets", "New England Patriots"]
    afcn_teams = ["Cincinnati Bengals", "Baltimore Ravens", "Cleveland Browns", "Pittsburgh Steelers"]
    afcs_teams = ["Tennessee Titans", "Jacksonville Jaguars", "Indianapolis Colts", "Houston Texans"]
    
    nfcw_teams = ["San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals", "Los Angeles Rams"]
    nfce_teams = ["Philadelphia Eagles", "Dallas Cowboys", "New York Giants", "Washington Commanders"]
    nfcn_teams = ["Minnesota Vikings", "Detroit Lions", "Green Bay Packers", "Chicago Bears"]
    nfcs_teams = ["Tampa Bay Buccaneers", "Carolina Panthers", "New Orleans Saints", "Atlanta Falcons"]
    
    conf_list = ['AFC West', 'AFC East', 'AFC North', 'AFC South',
                 'NFC West', 'NFC East', 'NFC North', 'NFC South']
    
    teams_list = [afcw_teams, afce_teams, afcn_teams, afcs_teams,
                  nfcw_teams, nfce_teams, nfcn_teams, nfcs_teams]
    
    # Generate Conference comparisons.
    for conf, t in zip(conf_list, teams_list):
        for ref in ref_list:
            fig, ax = plt.subplots(2, 1, sharex=False, figsize=(10., 9.0), dpi=120)
            for i, fav in enumerate([True, False]):
                fav_str = 'Favorites' if fav else 'Dogs'
                df_home_fav = ats_ref_analysis(data, 
                                               ref=ref, 
                                               teams=t, 
                                               atHome=True, 
                                               favorite=fav, 
                                               years='all', 
                                               )
                
                df_away_fav = ats_ref_analysis(data, 
                                               ref=ref, 
                                               teams=t, 
                                               atHome=False, 
                                               favorite=fav, 
                                               years='all', 
                                               )
                
                plot_dict = {key: [] for key in df_home_fav.index }
                
                if not df_home_fav.empty:                    
                    [plot_dict[k].append(df_home_fav.ATS[k] * 100) for k in df_home_fav.index]
                    [plot_dict[k].append(df_away_fav.ATS[k] * 100) for k in df_away_fav.index]
                    
                    bar_plot(ax[i], plot_dict, group_stretch=0.8, bar_stretch=0.75, legend=True,
                             x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                             bar_labeler=lambda k, i, s: str(int(s)))
                    
                    ax[i].set_title(' '.join((conf, ' ATS as '+fav_str+' with', ref, 'Officiating')))
                    
                    ax[i].set_ylabel("Spread Covered [%]")
                    ax[i].set_yticks(np.arange(0, 110, 10))
                    ax[i].patch.set_edgecolor('k')
                    
                    plt.savefig('output/' + ref+ '/' + '_'.join((ref.split(' ')[-1], conf)) + '.png')


def generate_conference_comparison_noref(data):
    afcw_teams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Denver Broncos']    
    afce_teams = ["Buffalo Bills", "Miami Dolphins", "New York Jets", "New England Patriots"]
    afcn_teams = ["Cincinnati Bengals", "Baltimore Ravens", "Cleveland Browns", "Pittsburgh Steelers"]
    afcs_teams = ["Tennessee Titans", "Jacksonville Jaguars", "Indianapolis Colts", "Houston Texans"]
    
    nfcw_teams = ["San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals", "Los Angeles Rams"]
    nfce_teams = ["Philadelphia Eagles", "Dallas Cowboys", "New York Giants", "Washington Commanders"]
    nfcn_teams = ["Minnesota Vikings", "Detroit Lions", "Green Bay Packers", "Chicago Bears"]
    nfcs_teams = ["Tampa Bay Buccaneers", "Carolina Panthers", "New Orleans Saints", "Atlanta Falcons"]
    
    conf_list = ['AFC West', 'AFC East', 'AFC North', 'AFC South',
                 'NFC West', 'NFC East', 'NFC North', 'NFC South']
    
    teams_list = [afcw_teams, afce_teams, afcn_teams, afcs_teams,
                  nfcw_teams, nfce_teams, nfcn_teams, nfcs_teams]
    
    
    for conf, t in zip(conf_list, teams_list):
        fig, ax = plt.subplots(2, 1, sharex=False, figsize=(9.0, 9.0), dpi=120)
        
        for i, fav in enumerate([True, False]):
            fav_str = 'Favorites' if fav else 'Dogs'
        # Generate Conference comparisons.
            df_home_fav = ats_no_ref(data, 
                                     teams=t, 
                                     atHome=True, 
                                     favorite=fav, 
                                     year_range_list=[]
                                     )
            
            df_away_fav = ats_no_ref(data, 
                                     teams=t, 
                                     atHome=False, 
                                     favorite=fav, 
                                     year_range_list=[], 
                                     )
            
            plot_dict = {key: [] for key in df_home_fav.index }
            
            if not df_home_fav.empty:
                # fig = plt.figure(figsize=(12.0, 5.5), dpi=120)
                # ax = fig.add_subplot(111)
                
                [plot_dict[k].append(df_home_fav.ATS[k] * 100) for k in df_home_fav.index]
                [plot_dict[k].append(df_away_fav.ATS[k] * 100) for k in df_away_fav.index]
                
                bar_plot(ax[i], plot_dict, group_stretch=0.8, bar_stretch=0.75, legend=True,
                         x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                         bar_labeler=lambda k, i, s: str(int(s)))
                
                ax[i].set_title(' '.join((conf, 'Performance ATS as '+fav_str)))
                
                ax[i].set_ylabel("Spread Covered [%]")
                ax[i].set_yticks(np.arange(0, 110, 10))
                ax[i].patch.set_edgecolor('k')
                
        plt.savefig('output/' + conf + '.png')
        

def generate_conference_comparison_noref_bigplot(data):
    afcw_teams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Denver Broncos']    
    afce_teams = ["Buffalo Bills", "Miami Dolphins", "New York Jets", "New England Patriots"]
    afcn_teams = ["Cincinnati Bengals", "Baltimore Ravens", "Cleveland Browns", "Pittsburgh Steelers"]
    afcs_teams = ["Tennessee Titans", "Jacksonville Jaguars", "Indianapolis Colts", "Houston Texans"]
    
    nfcw_teams = ["San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals", "Los Angeles Rams"]
    nfce_teams = ["Philadelphia Eagles", "Dallas Cowboys", "New York Giants", "Washington Commanders"]
    nfcn_teams = ["Minnesota Vikings", "Detroit Lions", "Green Bay Packers", "Chicago Bears"]
    nfcs_teams = ["Tampa Bay Buccaneers", "Carolina Panthers", "New Orleans Saints", "Atlanta Falcons"]
    
    afc_list = ['AFC West', 'AFC East', 'AFC North', 'AFC South']
    afc_teams = [afcw_teams, afce_teams, afcn_teams, afcs_teams]
    
    nfc_list =  ['NFC West', 'NFC East', 'NFC North', 'NFC South']
    nfc_teams = [nfcw_teams, nfce_teams, nfcn_teams, nfcs_teams]
    
    conf_name = ['AFC', 'NFC']
    conf_labels = [afc_list, nfc_list]
    conf_teams = [afc_teams, nfc_teams]
    
    for name, lbl, teams in zip(conf_name, conf_labels, conf_teams):
        fig, ax = plt.subplots(2, 4, sharex=False, figsize=(27, 12.0), dpi=120)
        # fig.tight_layout()
        for i, (conf, t) in enumerate(zip(lbl, teams)):
            
            for j, fav in enumerate([True, False]):
                fav_str = 'Favorites' if fav else 'Dogs'
            # Generate Conference comparisons.
                df_home_fav = ats_no_ref(data, 
                                         teams=t, 
                                         atHome=True, 
                                         favorite=fav, 
                                         year_range_list=[]
                                         )
                
                df_away_fav = ats_no_ref(data, 
                                         teams=t, 
                                         atHome=False, 
                                         favorite=fav, 
                                         year_range_list=[], 
                                         )
                
                plot_dict = {key: [] for key in df_home_fav.index }
                
                if not df_home_fav.empty:
                    
                    [plot_dict[k].append(df_home_fav.ATS[k] * 100) for k in df_home_fav.index]
                    [plot_dict[k].append(df_away_fav.ATS[k] * 100) for k in df_away_fav.index]
                    
                    bar_plot(ax[j][i], plot_dict, group_stretch=0.8, bar_stretch=0.75, legend=True,
                             x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                             bar_labeler=lambda k, i, s: str(int(s)))
                    
                    ax[j][i].set_title(' '.join((conf, 'ATS as '+fav_str)))
                    
                    ax[j][i].set_ylabel("Spread Covered [%]")
                    ax[j][i].set_yticks(np.arange(0, 110, 10))
                    ax[j][i].patch.set_edgecolor('k')
                    
        plt.savefig('output/' + name + '.png')


def generate_interesting_comparisons(data, ref_list, favorite=True, favorite_str=''):   
    teams_list = ['League', 'New England Patriots', 'Kansas City Chiefs', 'Los Angeles Chargers', 'Buffalo Bills']
    year_list = ['all', '2001-2019', '2013-2022', '2020-2023', '2018-2023']

    for ref in ref_list:
        df_home_fav = ats_indv_ref(data, 
                                   ref, 
                                   teams=teams_list,
                                   year_range_list=year_list, 
                                   atHome=True, 
                                   favorite=favorite
                                   )
        
        df_away_fav = ats_indv_ref(data, 
                                   ref, 
                                   teams=teams_list,
                                   year_range_list=year_list, 
                                   atHome=False, 
                                   favorite=favorite
                                   )
        
        plot_dict = {key: [] for key in df_home_fav.index }
        
        if not df_home_fav.empty:
            fig = plt.figure(figsize=(18.0, 3.5), dpi=120)
            ax = fig.add_subplot(111)
            
            [plot_dict[k].append(df_home_fav.ATS[k] * 100) for k in teams_list]
            [plot_dict[k].append(df_away_fav.ATS[k] * 100) for k in teams_list]
            
            bar_plot(ax, plot_dict, group_stretch=0.8, bar_stretch=0.75, legend=True,
                     x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                     bar_labeler=lambda k, i, s: str(int(s)))
            
            ax.set_xticklabels(['Allen-Era Buffalo Bills (2018-2023)',
                                'Reid-Era Kansas City Chiefs (2013-2023)',
                                'Herbert-Era Los Angeles Chargers (2020-2023)',
                                'Brady-Era New England Patriots (2001-2019)'])
            
            ax.set_title(' '.join(('Performance ATS as '+fav_str+' with', ref, 'Officiating')))
            ax.set_ylabel("Spread Covered [%]")
            ax.set_yticks(np.arange(0, 130, 10))
            ax.patch.set_edgecolor('k')
            
            plt.savefig('output/interesting_plots/' + ref+ '/' + '_'.join(('Interesting', ref.split(' ')[-1], fav_str)) + '.png')
            
            
def generate_team_comparisons(data):   
    teams_list = ['League', 'New England Patriots', 'Kansas City Chiefs', 'Cincinnati Bengals', 'Buffalo Bills']
    year_list = ['all', '2001-2019', '2018-2022', '2020-2023', '2018-2023']

    fig, ax = plt.subplots(2, 1, sharex=False, figsize=(13.5, 9.0), dpi=120)
    fig1, ax1 = plt.subplots(2, 1, sharex=False, figsize=(13.5, 9.0), dpi=120)
    
    for i, fav in enumerate([True, False]):
        fav_str = 'Favorites' if fav else 'Dogs'
        
        df_home_fav = ats_no_ref(data, 
                                 teams=teams_list,
                                 year_range_list=year_list, 
                                 atHome=True, 
                                 favorite=fav
                                 )
        
        df_away_fav = ats_no_ref(data, 
                                 teams=teams_list,
                                 year_range_list=year_list, 
                                 atHome=False, 
                                 favorite=fav
                                 )
        
        plot_dict = {key: [] for key in df_home_fav.index }
        
        if not df_home_fav.empty:
            # =============================================================================
            #             Plotting spread performance            
            # =============================================================================
            [plot_dict[k].append(df_home_fav.ATS[k] * 100) for k in teams_list]
            [plot_dict[k].append(df_away_fav.ATS[k] * 100) for k in teams_list]
            
            bar_plot(ax[i], plot_dict, group_stretch=0.8, bar_stretch=0.75, legend=True,
                     x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                     bar_labeler=lambda k, i, s: str(int(s)), 
                     bar_labeler_text=['Home','Away'], barlbl_add='%')
            
            ax[i].set_xticklabels(['Allen-Era Bills (2018-2023)',
                                   'Burrow-Era Bengals (2020-2023)',
                                   'Mahomes-Era Chiefs (2018-2023)',
                                   'League Average',
                                   'Brady-Era Patriots (2001-2019)'])
            
            ax[i].set_title(' '.join(('Performance ATS as ' + fav_str)))
            ax[i].set_ylabel("Spread Covered [%]")
            ax[i].set_yticks(np.arange(0, 110, 10))
            ax[i].patch.set_edgecolor('k')
            fig.tight_layout()
            
            # =============================================================================
            #             Average Penalty Yards as Home-Favorites vs Opp
            # =============================================================================
            teams_list2 = ['League', 'New England Patriots', 'Kansas City Chiefs', 'Cincinnati Bengals', 'Buffalo Bills']
            year_list2 = ['all', '2001-2019', '2018-2022', '2020-2023', '2018-2023']
            
            df_home_fav = ats_no_ref(data, 
                                     teams=teams_list2,
                                     year_range_list=year_list2, 
                                     atHome=True, 
                                     favorite=fav
                                     )
            
            df_away_fav = ats_no_ref(data, 
                                     teams=teams_list2,
                                     year_range_list=year_list2, 
                                     atHome=False, 
                                     favorite=fav
                                     )
            
            plot_dict = {key: [] for key in df_home_fav.index }
            [plot_dict[k].append(df_home_fav.TmAveragePenaltyYards[k]) for k in teams_list2]
            [plot_dict[k].append(df_home_fav.OppAveragePenaltyYards[k]) for k in teams_list2]
            
            [plot_dict[k].append(df_away_fav.OppAveragePenaltyYards[k]) for k in teams_list2]
            [plot_dict[k].append(df_away_fav.TmAveragePenaltyYards[k]) for k in teams_list2]
            
            
            bar_plot(ax1[i], plot_dict, group_stretch=0.8, bar_stretch=0.8, legend=True,
                      x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
                      bar_labeler=lambda k, i, s: str(int(s)), 
                      bar_labeler_text=['Home', 'Opp.', 'Away', 'Opp'], barlbl_add=' yds')
            
            ax1[i].set_xticklabels(['Allen-Era Bills (2018-2023)',
                                   'Burrow-Era Bengals (2020-2023)',
                                   'Mahomes-Era Chiefs (2018-2023)',
                                   'League Average',
                                   'Brady-Era Patriots (2001-2019)'])
            axis_list = ['Team', 'Opponent']
            ax1[i].set_title('Penalty Yards as ' + fav_str)
            ax1[i].set_ylabel("Average Penalty Yards [Yards]")
            ax1[i].set_yticks(np.arange(0, 110, 10))
            ax1[i].patch.set_edgecolor('k')
            fig1.tight_layout()
            
            # # =============================================================================
            # #             Average Penalty Yards as Home-Favorites vs Opp
            # # =============================================================================
            # teams_list2 = ['League', 'New England Patriots', 'Tampa Bay Buccaneers']
            # year_list2 = ['all', '2001-2019', '2020-2023']
            
            # df_home_fav = ats_no_ref(data, 
            #                          teams=teams_list2,
            #                          year_range_list=year_list2, 
            #                          atHome=True, 
            #                          favorite=fav
            #                          )
            
            # df_away_fav = ats_no_ref(data, 
            #                          teams=teams_list2,
            #                          year_range_list=year_list2, 
            #                          atHome=False, 
            #                          favorite=fav
            #                          )
            
            # plot_dict = {key: [] for key in df_home_fav.index }
            # [plot_dict[k].append(df_home_fav.TmAveragePenaltyYards[k]) for k in teams_list2]
            # [plot_dict[k].append(df_home_fav.OppAveragePenaltyYards[k]) for k in teams_list2]
            
            # [plot_dict[k].append(df_away_fav.OppAveragePenaltyYards[k]) for k in teams_list2]
            # [plot_dict[k].append(df_away_fav.TmAveragePenaltyYards[k]) for k in teams_list2]
            
            
            # bar_plot(ax1[i], plot_dict, group_stretch=0.8, bar_stretch=0.8, legend=True,
            #           x_labels=True, label_fontsize=8, barlabel_offset=0.05,colors=Teams,
            #           bar_labeler=lambda k, i, s: str(int(s)), 
            #           bar_labeler_text=['Home', 'Opp.', 'Away', 'Opp'], barlbl_add=' yds')
            
            # ax1[i].set_xticklabels(['League Average',
            #                         'Brady-Era Patriots (2001-2019)',
            #                         'Brady-Era Buccs (2020-2023)',])
            # axis_list = ['Team', 'Opponent']
            # ax1[i].set_title('Brady-Era Penalty Yards as ' + fav_str)
            # ax1[i].set_ylabel("Average Penalty Yards [Yards]")
            # ax1[i].set_yticks(np.arange(0, 110, 10))
            # ax1[i].patch.set_edgecolor('k')
            # fig1.tight_layout()
            
            # plt.savefig('output/interesting_plots/' + 'Interesting_AllRefs' + '.png')


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, x[i]+1, int(y[i]), ha='center')


if __name__ == "__main__":
    plt.close('all')
    
    xlsx = pd.read_excel("data/master_NFL2000-2022.xlsx")
    xlsx = xlsx.fillna('')
    
    referee_list = list(set(xlsx.Referee))
    referee_list = [x for x in referee_list if x]

    active_refs = [
        'Clete Blakeman',
        'Jerome Boger',
        'Carl Cheffers',
        'Tony Corrente',
        'Shawn Hochuli',
        'Bill Vinovich',
        'Land Clark',
        'Ron Torbert',
        'Adrian Hill',
        'Craig Wrolstad',
        'Scott Novak',
        'John Hussey',
        'Brad Rodgers',
        'Alex Kemp',
        'Clay Martin',
        'Shawn Smith',
        'Brad Allen',
        'Tra Blake',
        'Don Willard',
        'Walt Anderson'
        ]
    
    # generate_conference_comparison_noref(data=xlsx)
    # generate_conference_comparison_noref_bigplot(data=xlsx)
    # generate_conference_comparison(data=xlsx, ref_list=active_refs)
    # generate_team_comparisons(xlsx)
    
    for fav in [True, False]:
        fav_str = 'Favorites' if fav else 'Dogs'
        generate_conference_comparison(data=xlsx, 
                                        ref_list=active_refs,
                                        favorite=fav, 
                                        favorite_str=fav_str
                                        )
