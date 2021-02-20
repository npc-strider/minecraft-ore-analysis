
import matplotlib.pyplot as plt
from cycler import cycler

from matplotlib.ticker import MultipleLocator
import json


with open('./RESULTS_ALL__NEW_ORGEN_TEST.json', 'r') as file:
    NEW_DATA = json.loads(file.read())
with open('./RESULTS_ALL__OLD_ORE_GEN.json', 'r') as file:
    OLD_DATA = json.loads(file.read())

def list_distribution(block, data):
    return [ y[block] if block in y else 0 for y in data ]

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
ABSOLUTE_BLOCKS_NEW = ABSOLUTE_BLOCKS_OLD+[
    'minecraft:copper_ore',
    'minecraft:amethyst_block',
]

RELATIVE_BLOCKS_OLD = ABSOLUTE_BLOCKS_OLD+[ #BLOCKS to show in the relative frequency distribution.
    'minecraft:lava'
]
RELATIVE_BLOCKS_NEW = RELATIVE_BLOCKS_OLD+[
    'minecraft:copper_ore',
    'minecraft:amethyst_block',
]

x = list(range(-64,321))

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
def gen_maxis(axis):
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

#   quick/hackily converted the script to a function
def main(style, show_bounds, linewidth, dpi, size):
    plt.style.use(style)

    #
    #   abs frequency.
    #
    fig0, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    set_figure(fig0, dpi, size)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig0.suptitle('New ore generation - Absolute frequency - 1024*1024 area sample size')

    plot_absolute(ax1, ABSOLUTE_BLOCKS_OLD, OLD_DATA, [-64, 1], [256, 320], linewidth)
    plot_absolute(ax2, ABSOLUTE_BLOCKS_NEW, NEW_DATA, [0, 0], [0, 0], linewidth)

    gen_maxis(ax1)
    gen_maxis(ax2)

    if show_bounds: add_bounds(ax1)
    ax1.set_title("1.16.5 generation")
    ax1.set_ylabel(r'$\Sigma ore$')
    ax1.set_xlabel('Elevation above void (m)')

    ax2.set_title("21w07a generation")
    ax2.set_ylabel(r'$\Sigma ore$')
    ax2.set_xlabel('Elevation above grimstone (m)')

    cfg_naxis([ax1, ax2])

    #
    #   Let's also show relative frequency.
    #
    fig1, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    set_figure(fig1, dpi, size)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig1.suptitle('New ore generation - Relative frequency - 1024*1024 area sample size')

    plot_relative(ax1, RELATIVE_BLOCKS_OLD, OLD_DATA, [-64, 1], [256, 320], linewidth)
    plot_relative(ax2, RELATIVE_BLOCKS_NEW, NEW_DATA, [0, 0], [0, 0], linewidth)

    if show_bounds: add_bounds(ax1)
    ax1.set_title("1.16.5 generation")
    ax1.set_ylabel('Relative Frequency (%)')
    ax1.set_xlabel('Elevation above void (m)')

    ax2.set_title("21w07a generation")
    ax2.set_ylabel('Relative Frequency (%)')
    ax2.set_xlabel('Elevation above grimstone (m)')

    cfg_naxis([ax1, ax2])

    return [plt, [fig0, fig1]]