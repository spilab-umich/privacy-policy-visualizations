from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, TapTool, OpenURL, NumeralTickFormatter, CategoricalColorMapper
from bokeh.transform import factor_mark
import pandas as pd

def generate_scatter_plot(policydf, industries, colors, markers):
    tt = tooltips = [("Name", "@name"), ("Industry", "@industry"), ("URL", "@url")]

    if (len(industries)!=len(colors)) or (len(industries)!=len(markers)):
        raise Exception("Number of industries does not match the number of markers and/or colors provided for the scatterplot.")

    TOOLS = '''hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help'''
    source = ColumnDataSource(policydf)

    color_mapper = CategoricalColorMapper(
        factors=industries,
        palette=colors)

    shape_markers = markers

    p = figure(title="Length vs Vagueness",
           x_axis_label='Policy Length',
           y_axis_label='Policy Vagueness',
           tools=TOOLS)
    p.xaxis[0].formatter = NumeralTickFormatter(format="0")

    hover = HoverTool(tooltips=tt)
    p.scatter(y='vagueness',
          x='length',
          size=10,
          source=source,
          color={
              'field': 'industry',
              'transform': color_mapper
          },
          marker=factor_mark('industry', shape_markers, industries),
          legend_group="industry")

    url = "@url"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.add_tools(hover)

    return p


def main():

    # Import data and put it into a dataframe
    df = pd.read_csv('samplerandompolicydata.csv')

    # Get list of industries and colors
    total_colors=['red', 'blue', 'green', 'grey', 'pink', 'purple', 'black', 'white', 'yellow', 'brown', 'orange']
    total_shape_markers = ['plus', 'circle_x', 'triangle', 'square', 'cross', 'diamond', 'hex', 'star', 'y', 'x', 'dot']

    industries = pd.unique(df['industry'])
    num_categories = len(industries)

    colors = total_colors[0:num_categories]
    shape_markers = total_shape_markers[0:num_categories]

    p=generate_scatter_plot(df,industries,colors,shape_markers)

    # Generates bokehrandomdata.html with the graph
    show(p)

    script, div = components(p)

    with open("scatterplotscript.html", "w") as f:
        f.write(script)

    with open("scatterplotdiv.html", "w") as g:
        g.write(div)


if __name__ == "__main__":
    main()

