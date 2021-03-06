## Run with a a working scipy stack (such as Anaconda)
"""
This script draws plots for the *_stats.yaml files generated by the StatsLogger

Usage: ipython draw_plots.py [statsfile]
"""

import yaml, scipy, pylab, sys
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.font_manager import FontProperties
from itertools import *

smoothed = True
WindowSize = 5

Colors = {
	'Imperative': 'Red',
	'Var': 'OrangeRed',
	'Signal': 'DodgerBlue',
	'Handler': 'Gold',
	'DEFAULT': 'LightGreen'}

def make_bars(stats, fileout):
	plt.figure()
	plt.subplot(1,1,1)
	
	def color((name, _)):
		for n, c in Colors.items():
			if n in name: return c
		else: return Colors['DEFAULT']

	types = sorted(stats['Node types'].items(), key=lambda (x, y): y)
	names = [x[0] for x in types]
	groups = groupby(types, color)	
	grouped = [(name, count, color) for (color, group) in groups for (name, count) in group]

	for i, (name, count, color) in enumerate(grouped):
		plt.barh(i, count, align='center', color = color)
	
	#plt.subplots_adjust(left=2.0)
	plt.yticks(range(len(names)), names)
	plt.title('Distribution of Reactives')
	plt.tight_layout()
	
	if fileout == 'show': plt.show()
	else: plt.savefig(fileout)

def make_graphs(stats, fileout):
	Gaussian = scipy.signal.gaussian(WindowSize, 2)
	Gaussian = Gaussian / sum(Gaussian)
	fontP = FontProperties()
	fontP.set_size('small')

	perRoundStats = [['Turns per round', 'Time per round'], ['Created nodes per round', 'Cumulative nodes per round'], ['Pulses per round']]
	for i, subset in enumerate(perRoundStats):
		plt.subplot(len(perRoundStats), 1, i + 1)
		for pr in subset:
			plot = stats[pr]
			if i == 0 and smoothed: plot = pylab.convolve(plot, Gaussian, 'same')
			plt.plot(plot, label=pr) # drawstyle = 'steps'
		plt.xlabel('Round')
		plt.legend(prop = fontP)

	if fileout == 'show': plt.show()
	else: plt.savefig(fileout)



if __name__ == '__main__':
	if len(sys.argv) <= 1:
		stats = yaml.load(file('test.yaml', 'r'))
		make_graphs(stats, 'show')
		make_bars(stats, 'show')
	else:
		infile = sys.argv[1]
		stats = yaml.load(file(infile, 'r'))
		origfile = infile.split('.')[0:-1]
		make_graphs(stats, ".".join(origfile + ['time', 'png']))
		make_bars(stats, ".".join(origfile + ['dist', 'png']))
