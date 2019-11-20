from IPython.display import HTML
import pygal
import pandas as pd
import numpy as np
import datetime

pd.set_option('plotting.backend', 'pandas_bokeh')
pd.plotting.output_notebook()

from bokeh.models.formatters import NumeralTickFormatter, PrintfTickFormatter
from bokeh.plotting import show

import altair as alt
alt.renderers.enable('kaggle')

def altair_format(df):
    """Wide-format to narrow-format"""
    return (
        df.reset_index()
        .melt('index', var_name='Factor', value_name='Amount')
        .rename(columns={'index':'Year'})
    )

def altair_outcomes_chart(df):
    return alt.Chart(df).mark_line(size=7, point=True).encode(
        x='Year:T',
        y='Amount:Q',
        color='Factor:N', 
        tooltip=['Year:T', 'Factor:N', alt.Tooltip('Amount:Q', format='$,.2f')]
    ).interactive()

def altair_wealth_chart(df):
    df = df.query('Factor == "wealth"')
    return alt.Chart(df).mark_area(opacity=0.4).encode(
        x='Year:T',
        y=alt.Y('Amount:Q', stack=None),
        color='Factor:N',
        tooltip=['Year:T', alt.Tooltip('Amount:Q', format='$,.2f')]
    ).interactive()

def bokeh_outcomes_chart(df):
    p = df.plot(kind='line', 
                show_figure=False,
                toolbar_location=None,
                panning=False,
                zooming=False,
                plot_data_points=True,
                plot_data_points_size=5
               )
    p.hover.tooltips = [('year', '$index')] + list(
        (c, f'£@{c}'+'{0,0}')
    for c in df.columns)
    p.hover.mode='mouse'
    p.yaxis[0].formatter = NumeralTickFormatter(format='£0,0')
    p.xaxis.major_label_orientation = 3.14/5
    p.legend.location = "top_left"
    # p.yaxis[0].formatter.use_scientific = False
    return p

def bokeh_wealth_chart(df):
    p = (df.wealth + df.cash_flow).rename('Net wealth').plot.line(
        show_figure=False,
        toolbar_location=None,
        hovertool_string=r"""<h4> Net wealth: </h4> £@{Net wealth}{0,0}""",
        panning=False,
        zooming=False
    )
    p.yaxis[0].formatter = NumeralTickFormatter(format='$0,0')
    p.xaxis.major_label_orientation = 3.14/5
    p.legend.location = "top_left"
    # p.yaxis[0].formatter.use_scientific = False
    return p

def pygal_outcomes_chart(df):
    line_chart = pygal.Line(dynamic_print_values=True, value_formatter=lambda x: f'£{x:,.0f}')
    line_chart.title = 'Investment Outcomes:'
    line_chart.x_labels = map(str, range(0, len(df)))

    line_chart = pygal.Line(dynamic_print_values=True, value_formatter=lambda x: f'£{x:,.0f}')
    for c in df.columns:
        line_chart.add(c, df[c])

    pygal_script = '<script type="text/javascript" src="http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js"></script>'
    return HTML(line_chart.render(is_unicode=True)+pygal_script)