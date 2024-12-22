import plotly.express as px
fig = px.bar(x=["a", "b", "c", "d"], y=[1,2,3,4])
fig.write_html("first_figure.html", auto_open=True)
#fig.show()