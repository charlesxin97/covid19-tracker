# resulting.py

import pandas as pd
from bokeh.models import DatePicker
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import Div, ColumnDataSource, HoverTool, SingleIntervalTicker, LinearAxis, Range1d
from bokeh.io import show
from bokeh.palettes import GnBu3, OrRd3
from bokeh.models.annotations import Title

from bokeh.io import show

# read data using pandas
data_total_url = "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-state-totals.csv"
data_total = pd.read_csv(data_total_url)
data_race_url = "https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-race-ethnicity.csv"
data_race = pd.read_csv(data_race_url)
latest_date = data_race['date'][0]

# title and reference
intro = Div(text="""This is a project for <b>visualization of covid-19 data</b>. Basically 3 questions can be answered by 
selecting the date in the <b>date picker</b>: <br>(1) Number of new covid-19 cases in CA on a particular day <br>
(2) For a particular day, what is the %percent cases by race compared to their representation in the
general population? <br>(3) For a particular day, what is the %percent deaths by race compared to their representation in the
general population? <br> The first question is answered in a <b>scatter</b> with one point and the second and third ones are answered in a <b>bar 
chart</b>. If there is no data in the figure, that means there is no available data for that figure on the selected date. <br> All data used is collected from <a href="https://github.com/datadesk/california-coronavirus-data">A Github 
repository having data from <b>LA-Times</b></a>. 
The latest update date is {}""".format(latest_date),
            width=1000, height=100)

# date picker
date_picker = DatePicker(title='Select a Date', value="2020-08-01", min_date="2020-08-01", max_date="2020-12-31")

# answers
selected_date = latest_date
description = Div(text="""New cases on {}""".format(selected_date),
            width=1000, height=100)
# p1
total_cases = data_total['confirmed_cases']
dates = data_total['date']
new_cases = []
for i in range(len(dates)):
	if dates[i] == selected_date:
		new_cases.append(total_cases[i] - total_cases[i + 1])
		new_cases.append(total_cases[i])
		new_cases.append(total_cases[i + 1])
		break
source_1 = ColumnDataSource(
	data=dict(
		x=[int(selected_date.replace('-', '')) % 10000],
		y=[int(new_cases[0])],
		date=[selected_date],
		td=[new_cases[1]],
		ld=[new_cases[2]]
	)
)

hover_1 = HoverTool(
	tooltips=[
		("date", "@date"),
		("new cases", "@y"),
		("cases (today, last day)", "(@td, @ld)"),
	]
)

p1 = figure(plot_width=300, plot_height=300, x_axis_type=None,
            tools=[hover_1], title="(Hover for more information)")
ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
ticker.desired_num_ticks = 1
x_axis = LinearAxis(ticker=ticker)
p1.add_layout(x_axis, 'below')
p1.circle('x', 'y', size=20, source=source_1)

# p2
dates_race = data_race['date']
result = {'asian': [], 'black': [], 'cdph-other': [], 'white': [], 'latino': [], 'other': []}
for k in result.keys():
	for i in range(len(dates_race)):
		if dates_race[i] == selected_date:
			if data_race['race'][i] == k and data_race['age'][i] == 'all':
				result[k].append(data_race['confirmed_cases_percent'][i])
				result[k].append(data_race['deaths_percent'][i])
				result[k].append(data_race['population_percent'][i])

categories = ['cases_percent', 'deaths_percent', 'population_percent']
races = ['Asian', 'Black', 'CDPH-other', 'White', 'Latino', 'Other']

source_2 = ColumnDataSource(
	data=dict(
		races=races,
		cases_percent=[result['asian'][0], result['black'][0], result['cdph-other'][0], result['white'][0],
		               result['latino'][0], result['other'][0]],
		deaths_percent=[result['asian'][1], result['black'][1], result['cdph-other'][1], result['white'][1],
		                result['latino'][1], result['other'][1]],
		population_percent=[result['asian'][2], result['black'][2], result['cdph-other'][2], result['white'][2],
		                    result['latino'][2], result['other'][2]],
		date=[selected_date, selected_date, selected_date, selected_date, selected_date, selected_date]
	)
)

hover_2 = HoverTool(
	tooltips=[
		("race", "@races"),
		("date", "@date"),
		("cases_percent", "@cases_percent"),
		("deaths_percent", "@deaths_percent"),
		("population_percent", "@population_percent")
	]
)
p2 = figure(y_range=races, plot_height=250, tools=[hover_2], x_range=(-1, 4),
            title="Percentage of total confirmed cases, deaths and "
                  "population for different races")

p2.hbar_stack(categories, y='races', height=0.9, color=GnBu3, source=source_2,
              legend_label=["%s" % x for x in categories])


p2.y_range.range_padding = 0.1
p2.ygrid.grid_line_color = None
p2.legend.location = "center_right"


# call back function


def call_back(attr, old, new):
	global selected_date
	selected_date = date_picker.value
	description.text = "New cases on {}".format(selected_date)

	# p1
	new_new_cases = []
	flag_1 = 0
	for i in range(len(dates)):
		if dates[i] == selected_date:
			flag_1 = 1
			new_new_cases.append(total_cases[i] - total_cases[i + 1])
			new_new_cases.append(total_cases[i])
			new_new_cases.append(total_cases[i + 1])
			break
	new_source_1_data = dict(
			x=[int(selected_date.replace('-', '')) % 10000],
			y=[int(new_new_cases[0])],
			date=[selected_date],
			td=[new_new_cases[1]],
			ld=[new_new_cases[2]]
		)
	source_1.data = new_source_1_data
	print(new_new_cases, flag_1, p1.title.text, p1.x_range.start, p1.x_range.end)

	#p2
	new_result = {'asian': [], 'black': [], 'cdph-other': [], 'white': [], 'latino': [], 'other': []}
	flag_2 = 0
	for k in new_result.keys():
		for i in range(len(dates_race)):
			if dates_race[i] == selected_date:
				flag_2 = 1
				if data_race['race'][i] == k and data_race['age'][i] == 'all':
					new_result[k].append(data_race['confirmed_cases_percent'][i])
					new_result[k].append(data_race['deaths_percent'][i])
					new_result[k].append(data_race['population_percent'][i])
	if flag_2 == 0:
		new_result = new_result = {'asian': [0,0,0], 'black': [0,0,0], 'cdph-other': [0,0,0], 'white': [0,0,0], 'latino': [0,0,0], 'other': [0,0,0]}

	new_source_2_data=dict(
		races=races,
		cases_percent=[new_result['asian'][0], new_result['black'][0], new_result['cdph-other'][0], new_result['white'][0],
		               new_result['latino'][0], new_result['other'][0]],
		deaths_percent=[new_result['asian'][1], new_result['black'][1], new_result['cdph-other'][1], new_result['white'][1],
		                new_result['latino'][1], new_result['other'][1]],
		population_percent=[new_result['asian'][2], new_result['black'][2], new_result['cdph-other'][2], new_result['white'][2],
		                    new_result['latino'][2], new_result['other'][2]],
		date=[selected_date, selected_date, selected_date, selected_date, selected_date, selected_date]
	)
	source_2.data = new_source_2_data
	print(new_result, flag_2)


date_picker.on_change("value", call_back)
# layout
curdoc().add_root(column(intro, date_picker, description, p1, p2))

#### labels and legends
