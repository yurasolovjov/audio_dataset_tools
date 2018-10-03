import os
import plotly
import plotly.graph_objs as go

def histogram(data, outcatalog = ""):

    data = [
        go.Histogram(
            histfunc="count",
            x=data,
            name="count"
        ),
    ]

    plotly.offline.plot({
        "data": data,
        "layout": go.Layout(title="Histogram")
    }, auto_open=True)

    pass

