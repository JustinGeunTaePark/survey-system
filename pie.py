"""
===============
Basic pie chart
===============

Demo of a basic pie chart plus a few additional features.

In addition to the basic pie chart, this demo shows a few optional features:

    * slice labels
    * auto-labeling the percentage
    * offsetting a slice with "explode"
    * drop-shadow
    * custom start angle

Note about the custom start angle:

The default ``startangle`` is 0, which would start the "Frogs" slice on the
positive x-axis. This example sets ``startangle = 90`` such that everything is
rotated counter-clockwise by 90 degrees, and the frog slice starts on the
positive y-axis.
"""
import matplotlib
import matplotlib.pyplot as plt
import mpld3
from mvc import *
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
def pie(course, question):
	new_dict = {}
	labels = []
	sizes = []
	explode = []
	controller = Controller()
	retVal = controller.return_answers(course)
	if not retVal:
		return 0

	for val in retVal:
		if question == val[3]:
			if val[4] not in labels:
				new_dict[val[4]] = 1
				explode.append(0)
			else:
				new_dict[val[4]] += 1
	
	labels = new_dict.keys()
	sizes = list(new_dict.values())
	print(labels)
	print(sizes)
	print(explode)

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        	shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	
	#plt.show()
	htmlOutput = mpld3.fig_to_html(fig1)
	#print("test", htmlOutput)
	return htmlOutput
