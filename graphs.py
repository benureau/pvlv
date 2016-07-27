import numpy as np
import colorsys

from bokeh import io
from bokeh import plotting as bkp
from bokeh.core.properties import value
from bokeh.models import FixedTicker
from bokeh.models.mappers import LinearColorMapper

import ipywidgets.widgets
from ipywidgets.widgets import fixed, IntSlider, FloatSlider, SelectionSlider


    ## Disable autoscrolling

from IPython.display import display, Javascript

disable_js = """
IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
}
"""
display(Javascript(disable_js))


    ## Larger labels

from IPython.display import HTML

display(HTML('''<style>
    .widget-label { min-width: 20ex !important; }
</style>'''))


    ## Load bokeh for jupyter

bkp.output_notebook(hide_banner=True)


    ## Better default figures

def tweak_fig(fig):
    tight_layout(fig)
    disable_minor_ticks(fig)
    disable_grid(fig)
    fig.toolbar.logo = None

def tight_layout(fig):
    fig.min_border_top    = 35
    fig.min_border_bottom = 35
    fig.min_border_right  = 35
    fig.min_border_left   = 35

def disable_minor_ticks(fig):
    #fig.axis.major_label_text_font_size = value('8pt')
    fig.axis.minor_tick_line_color = None
    fig.axis.major_tick_in = 0

def disable_grid(fig):
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None


def figure(*args, **kwargs):
    fig = bkp.figure(*args, **kwargs)
    tweak_fig(fig)
    return fig


    ## Removing returns

def show(*args, **kwargs):
    bkp.show(*args, **kwargs)

def interact(*args, **kwargs):
    ipywidgets.widgets.interact(*args, **kwargs)

def select(name, options):
    return SelectionSlider(description=name,  options=list(options))

    ## Graphs

def unit_activity(data):
    """Display graph of best choice"""

    fig = figure(x_range=[0, 200], y_range=[-0.5, 1.0],
                 plot_width=400, plot_height=400, tools="")
    fig.title.text = "Unit activity"

    for name, color in [('net', 'red'), ('v_m', 'yellow'),
                        ('I_net', 'orange'), ('act', 'green')]:
        fig.line(range(201), data[name], color=color, legend=name, line_width=2)

    bkp.show(fig)
