
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.ticker import MultipleLocator

from copy import deepcopy
import json

DATA_FILES = [
    './RESULTS_ALL__1.16.5.json',
    './RESULTS_ALL__21w07a.json',
    './RESULTS_ALL__21w08b.json'
]

DATA = []

for datafile in DATA_FILES:
    with open(datafile, 'r') as file:
        DATA.append(json.loads(file.read()))

def list_distribution(blocks, data):
    slices = []
    for yslice in data:
        c = 0
        for block in blocks.split('||'):
            if block in yslice: c += yslice[block]
        slices.append(c)
    return slices   
    # return [ y[block] if block in y else 0 for y in data ]

ABSOLUTE_BLOCKS_OLD = [
    'minecraft:diamond_ore',
    'minecraft:redstone_ore',
    'minecraft:emerald_ore',
    'minecraft:gold_ore',
    'minecraft:lapis_ore',
    'minecraft:iron_ore',
    'minecraft:coal_ore',
    # 'minecraft:lava'
]
ABSOLUTE_BLOCKS_NEW = [
    'minecraft:diamond_ore||minecraft:deepslate_diamond_ore',
    'minecraft:redstone_ore||minecraft:deepslate_redstone_ore',
    'minecraft:emerald_ore',
    'minecraft:gold_ore||minecraft:deepslate_gold_ore',
    'minecraft:lapis_ore',
    'minecraft:iron_ore||minecraft:deepslate_iron_ore',
    'minecraft:coal_ore',
    'minecraft:copper_ore',
    'minecraft:amethyst_block',
]

RELATIVE_BLOCKS_OLD = ABSOLUTE_BLOCKS_OLD+[ #BLOCKS to show in the relative frequency distribution.
    'minecraft:lava'
]
RELATIVE_BLOCKS_NEW = deepcopy(ABSOLUTE_BLOCKS_NEW)
RELATIVE_BLOCKS_NEW.insert(-2, 'minecraft:lava')

ABSOLUTE_AX_PROPERTIES = [
    {"title":"1.16.5 generation", "ylabel":r'$\Sigma ore$', "xlabel":'Elevation above void (m)'},
    {"title":"21w07a generation", "ylabel":r'$\Sigma ore$', "xlabel":'Elevation above grimstone (m)'},
    {"title":"21w08b generation", "ylabel":r'$\Sigma ore$', "xlabel":'Elevation above grimstone (m)'}
]
RELATIVE_AX_PROPERTIES = [
    {"title":"1.16.5 generation", "ylabel":'Relative Frequency (%)', "xlabel":'Elevation above void (m)'},
    {"title":"21w07a generation", "ylabel":'Relative Frequency (%)', "xlabel":'Elevation above grimstone (m)'},
    {"title":"21w08b generation", "ylabel":'Relative Frequency (%)', "xlabel":'Elevation above grimstone (m)'}
]

x = list(range(-64,321))

#
#
#

def cfg_naxis(axes):
    for axis in axes:
        axis.grid(True, color='white', linewidth=0.2, linestyle='--', which="major")
        for line in axis.legend(loc='upper right').get_lines():
            line.set_linewidth(2.0)
        axis.set_xticks(x[::8]+[x[-1]])
        axis.minorticks_on()    
        axis.xaxis.set_tick_params(labelbottom=True)
        axis.yaxis.set_tick_params(labelbottom=True)
        axis.set_ylim(bottom=0.0)
        axis.set_xlim(left=-64,right=320)
        axis.xaxis.set_minor_locator(MultipleLocator(1)) 

#   Conversions between ore/chunk and total (based on sample size.)
#   Radius of 512
sample_r = 512
def orechunk(y):
    return y / (2*sample_r/16)**2
def sigmaore(x):
    return x * (2*sample_r/16)**2
def gen_maxis(axes):
    for axis in axes:
        secax = axis.secondary_yaxis('right', functions=(orechunk, sigmaore))
        secax.minorticks_on()
        secax.set_ylabel(r'$ore\cdot chunk\_layer^{-1}$')

def set_figure(fig, dpi, size):
    fig.set_dpi(100)
    fig.set_figwidth(size[0])
    fig.set_figheight(size[1])

def add_bounds(axis):
    axis.axvspan(-64, 0, alpha=0.5, color='gray', hatch="/")
    axis.axvspan(256, 320, alpha=0.5, color='gray', hatch="/")

def plot_absolute(axis, blocks, data, padl, padu, width):
    [ axis.plot(x, [0 for x in range(padl[0],padl[1])]+list_distribution(ore, data)+[0 for x in range(padu[0],padu[1])], label=ore, linewidth=width) for ore in blocks]
def plot_relative(axis, blocks, data, padl, padu, width):
    [ axis.plot(x, [0 for x in range(padl[0],padl[1])]+[p/sum(tmp)*100 for p in tmp]+[0 for x in range(padu[0],padu[1])], label=ore, linewidth=width) for ore in blocks if (tmp := list_distribution(ore, data))]

def set_ax_properties(axes, ax_properties):
    i = 0
    for ax in axes:
        ax.set_title(ax_properties[i]['title'])
        ax.set_xlabel(ax_properties[i]['xlabel'])
        ax.set_ylabel(ax_properties[i]['ylabel'])
        i += 1

#   quick/hackily converted the script to a function
def main(style, show_bounds, linewidth, dpi, size):
    plt.style.use(style)

    #
    #   abs frequency.
    #
    
    fig0, axes = plt.subplots(
            len(DATA),
            sharex=True,
            sharey=True
        )
    set_figure(fig0, dpi, size)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig0.suptitle('New ore generation - Absolute frequency - 1024*1024 area sample size')

    plot_absolute(axes[0], ABSOLUTE_BLOCKS_OLD, DATA[0], [-64, 1], [256, 320], linewidth)
    _ = 1
    for data in DATA[1:]:
        plot_absolute(axes[_], ABSOLUTE_BLOCKS_NEW, data, [0, 0], [0, 0], linewidth)
        _ += 1

    gen_maxis(axes)
    if show_bounds: add_bounds(axes[0])
    set_ax_properties(axes, ABSOLUTE_AX_PROPERTIES)
    cfg_naxis(axes)

    #
    #   Let's also show relative frequency.
    #
    fig1, axes = plt.subplots(
            len(DATA),
            sharex=True,
            sharey=True
        )
    set_figure(fig1, dpi, size)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig1.suptitle('New ore generation - Relative frequency - 1024*1024 area sample size')

    plot_relative(axes[0], RELATIVE_BLOCKS_OLD, DATA[0], [-64, 1], [256, 320], linewidth)
    _ = 1
    for data in DATA[1:]:
        plot_relative(axes[_], RELATIVE_BLOCKS_NEW, data, [0, 0], [0, 0], linewidth)
        _ += 1
    
    if show_bounds: add_bounds(axes[0])
    set_ax_properties(axes, RELATIVE_AX_PROPERTIES)
    cfg_naxis(axes)

    return [plt, [fig0, fig1]]