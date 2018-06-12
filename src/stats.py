#!usr/bin/python

import os
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import csv
import datetime

"""
Functions to create graphs derived from data located in the CSV files.

@author Arthur De Araujo
@contact adearauj@buffalo.edu
@github github.com/wafflez180

Created: 06/07/2016
"""

    plotly.tools.set_credentials_file(username='yourUsername', api_key='yourApiKey')

    numOfContributions = [0] * 10000000

    if os.path.exists('../data/contributionTotals.csv'):
        indat = np.genfromtxt('../data/contributionTotals.csv', dtype=None, delimiter=',', names=True, encoding=None)
        totalContrib = np.atleast_1d(indat['totalContributions'])
        len_indat = indat.size
        # Loop through every total contribution entry
        for i in range(len_indat):
            numOfContributions[totalContrib[i]] += 1

    labels = []
    values = []

    for i in range(len(numOfContributions)):
        if numOfContributions[i] != 0:
            labels.append(str(i) + " texts")
            values.append(numOfContributions[i])


    trace = go.Pie(labels=labels, values=values, hole=.2,textposition='outside')

    py.plot([trace], filename='number_of_texts_per_unique_user')

    print("Done")



def create_user_station_contrib_bar_graph():

    plotlyTraces = []

    if os.path.exists('../data/contributionTotals.csv'):
        totalfile = open('../data/contributionTotals.csv', 'r')
        totalreader = csv.reader(totalfile, delimiter=',')
        firstrow = True
        for user in totalreader:
            if not firstrow:
                # Parse the contribution dict column
                contribution_dict_str = user[4].replace("-", ",").replace("\'", "\"")
                contribution_dict = json.loads(contribution_dict_str)
                if len(contribution_dict_str) > 2: #If there is at least one contribution
                    plotlyTraces.append(go.Bar(
                        x=list(contribution_dict.keys()),
                        y=list(contribution_dict.values()),
                        name=user[0]))
            firstrow = False
        totalfile.close()

    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=plotlyTraces, layout=layout)
    py.plot(fig, filename='stacked-bar')


def create_date_of_contrib_line_graph():

    all_dates_dict = dict()

    # Get all the contributions and place all of the dates into their respective list which is according to their state
    # Example: {"MI", [dates], "WA", [dates]}
    if os.path.exists('../data/contributionTotals.csv'):
        totalfile = open('../data/contributionTotals.csv', 'r')
        totalreader = csv.reader(totalfile, delimiter=',')
        firstrow = True
        for user in totalreader:
            if not firstrow:
                # Parse the contribution date dict column
                contribution_date_dict_str = user[5].replace("-", ",").replace("\'", "\"")
                contribution_date_dict = json.loads(contribution_date_dict_str)
                if len(contribution_date_dict_str) > 2: #If there is at least one contribution
                    for stationKey, dateListVal in contribution_date_dict.items():
                        state_abbreviation = stationKey[:2]

                        if state_abbreviation not in all_dates_dict: # If there is an entry with a new state abbrev, add it to the dictionary
                            all_dates_dict[state_abbreviation] = []

                        for dateNum in dateListVal:
                            all_dates_dict[state_abbreviation].append(datetime.datetime.fromtimestamp(dateNum))
            firstrow = False
        totalfile.close()

    plotly_traces = []

    # Go through each data entry and for each day, calculate the number of entries on that day
    for state, dates in all_dates_dict.items():
        dates.sort()

        plotly_dates = []
        plotly_num_texts = []

        current_day = 0
        prev_date = dates[0]
        for date in dates:
            if date.day != current_day:

                # Fill in 0s for each day between the old date and the new date.
                roundedA = date.replace(hour=0, minute=0, second=0, microsecond=0)
                roundedB = prev_date

                next_day = prev_date + datetime.timedelta(days=1)
                days_till_next_entry = (roundedA - roundedB).days
                for i in range(days_till_next_entry):
                    try:
                        plotly_dates.append(next_day)
                        plotly_num_texts.append(0)
                        next_day += datetime.timedelta(days=1)
                    except OverflowError: # date value out of range, ex: July 32nd
                        if next_day.month == 12:
                            next_day = next_day.replace(month=1)
                        else:
                            next_day = next_day.replace(month=next_day.month+1)

                current_day = date.day
                # Append the new date
                plotly_dates.append(date)
                plotly_num_texts.append(1)
            else:
                # If the new entry's date is on the same day, increment the day's num of texts
                plotly_num_texts[-1] += 1
                prev_date = date

        plotly_traces.append(go.Scatter(
            x=plotly_dates,
            y=plotly_num_texts,
            mode='lines+markers',
            name=state
        ))

    py.plot(plotly_traces, filename='line-mode')


