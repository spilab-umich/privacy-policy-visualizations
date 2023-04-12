from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, TapTool, OpenURL, NumeralTickFormatter, CategoricalColorMapper
from bokeh.transform import factor_mark
import pandas as pd
import json

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

    p = figure(title="Privacy Policy Length vs Vagueness",
           x_axis_label='Number of Words in the Policy',
           y_axis_label='Vagueness (as measured by METRIC)',
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

    p.legend.title = 'Industry Sector of Privacy Policy'

    return p






def generate_scatter_plot_json(data_list):
    # source = ColumnDataSource(policydf)
    source = ColumnDataSource(
        data=dict(length=[float(d[1]) for d in data_list], 
                  vague=[float(d[0]) for d in data_list],
                  url = [d[2] for d in data_list] 
                  )
                  )
    

    tt = tooltips = [("URL", "@url"), ("Length", "@length"), ("Vagueness", "@vague")]

    TOOLS = '''hover,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help'''

    p = figure(title="Privacy Policy Length vs Vagueness",
           x_axis_label='Number of Words in the Policy',
           y_axis_label='Vagueness (as measured by METRIC)',
           tools = TOOLS
           )
    
    p.scatter(y='vague',
          x='length',
          size=1,
          source=source
          )
    
    url = "@url"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    hover = HoverTool(tooltips=tt)
    p.add_tools(hover)

    return p







def main():

    # Import data and put it into a dataframe
    # df = pd.read_csv('samplerandompolicydata.csv') # --> From the csv

    # open file and read in string
    with open("visualization_data.json", 'r') as e:
        # json_str = e.read()
        data = json.load(e)


    nested_dicts = data.values()
    data_list = [(d['vague'], d['length'], d['url'], d['readability']) for d in nested_dicts]

    # df2 = pd.read_json(json_str)
    # group = df.groupby()
    # print(df2)
    # Get list of industries and colors
    # total_colors=['red', 'blue', 'green', 'grey', 'pink', 'purple', 'black', 'white', 'yellow', 'brown', 'orange']
    # total_shape_markers = ['plus', 'circle_x', 'triangle', 'square', 'cross', 'diamond', 'hex', 'star', 'y', 'x', 'dot']

    # industries = pd.unique(df['industry'])
    # num_categories = len(industries)

    # colors = total_colors[0:num_categories]
    # shape_markers = total_shape_markers[0:num_categories]

    # p=generate_scatter_plot(df,industries,colors,shape_markers)
    p=generate_scatter_plot_json(data_list)

    # Generates bokehrandomdata.html with the graph
    show(p)

    # script, div = components(p)

    # with open("scatterplotscript.html", "w") as f:
    #     f.write(script)

    # with open("scatterplotdiv.html", "w") as g:
    #     g.write(div)


if __name__ == "__main__":
    main()

