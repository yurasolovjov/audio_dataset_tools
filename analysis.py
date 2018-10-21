import os
import plotly
import plotly.graph_objs as go
from collections import Counter
import numpy as np

def histogram(data,hist_mean= True, filename = "tmp_histogram.html"):

    if hist_mean == True:

        cdata = Counter(data)

        mean_number_classes = np.asarray([cdata[x] for x in cdata]).mean()

        ldata = list()

        for name in cdata:

            if cdata[name] > mean_number_classes:
                ldata += list(Counter({name:cdata[name]}).elements())


        trace_mean_data = go.Histogram(histfunc="count", x=ldata, name="count" )


    trace_data = go.Histogram(histfunc="count", x=data, name="count", text="" )

    trace = [ trace_data, trace_mean_data]

    plotly.offline.plot({
        "data": trace,
        "layout": go.Layout(title="stack")
    }, auto_open=True, filename=filename)

    pass

def pie_chart(labels, values = None, filename = "tmp_pie_chart.html", textinfo = 'label+value'):

    if labels == None:
        raise Exception("Can not create pie chart, because labels is None")

    if values == None:

        data = Counter(labels)

        labels = list()
        values = list()

        for name in data:
            labels.append(name)
            values.append(data[name])

    trace = go.Pie(labels=labels, values=values,textfont=dict(size=20),hoverinfo='label+percent', textinfo=textinfo,
                   marker=dict(line=dict(color='#000000', width=2))
                   )

    plotly.offline.plot([trace], filename='basic_pie_chart')
    pass

