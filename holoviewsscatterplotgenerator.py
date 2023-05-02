import pandas as pd
import holoviews as hv
from holoviews import opts
from holoviews.operation.datashader import datashade, shade, dynspread, spread
from holoviews.operation.datashader import rasterize, ResamplingOperation
from holoviews.operation import decimate
hv.extension('bokeh')

from bokeh.sampledata.periodic_table import elements

from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource, TapTool, OpenURL, NumeralTickFormatter, CategoricalColorMapper
from bokeh.transform import factor_mark

import json
import datashader as ds


def create_hovertool(values):
    '''
    This function createś a hovertool object that can be added to plots, which allows the user to hover over a datapoint and there will be a small popup showing information (e.g., name of policy, url of policy, etc.) 

        Parameters:
            values (dict): A dictionary with what should be displayed to the user in the hover tool. It should be in the form "Key": "@value", where "Key" is the text shown to the user, and "value" is the column name of the information to be shown. For example, the entry "URL": "@url" means the text URL will be shown to the user followed by the url of the datapoint, which is under the column "url".
        
        Returns:
            hover (HoverTool): A HoverTool

    '''       
    tooltips = []

    for (k, v) in values.items():
        tooltips.append((k, v))
        
    hover = HoverTool(tooltips=tooltips)
    return hover


def create_taptool():
    '''
    This function createś a taptool object that, when added to a plot, allows you to click on a datapoint and it opens the url associated with that datapoint.

        Parameters:
            None
        
        Returns:
            taptool (TapTool): A TapTool object

    '''       
    
    url = "@url"
    taptool = TapTool()
    taptool.callback = OpenURL(url=url)
    return taptool


def generate_scatter_plot(source, xaxis, yaxis, median=0):
    '''
    Returns a Holoviews Point Plot showing policy data in a scatter plot format.

        Parameters:
            source (df): a dataframe with the appropiate data. It assumes it has a URL column for each entry.
            xaxis (str): a string showing what the x-axis variable should be.
            yaxis (str): A string indicating what the y-axis variable should be.
            median (int): An optional 0/1 flag. The default is 0. If set to a 1, the plot will have lines indicating the median values for the x and y variables.

        Returns:
            p (Points): A Holoviews Points object
    '''     
    # Make Hover Tool
    hover_opts = {
        'URL': '@url',
    }
    hover = create_hovertool(hover_opts)

    # Make Tap tool
    taptool = create_taptool()
    
    # Initial Variables (hardcoded for now)
    width = 1250
    height = 1000
    size = 5
    # maxvalues = source.max()
    # maxx = maxvalues[xaxis]
    # maxy = maxvalues[yaxis]
    maxx = 27000
    maxy=1

    # Create scatterplot (technically 'points' in holoviews) and customize with options, including size of canvas, tools in the graph, and the size of the individual dots on the scatter plot.
    p = hv.Points(source, [xaxis, yaxis])
    p.opts(width=width, height=height, tools=[hover, taptool], size=size, xlim=(0,maxx), ylim=(0,maxy))
    
    if median==0:
        return p
    
    # Calculate median and plot it as lines on the graph
    medianvalues = source.median()
    mdx = medianvalues[xaxis]
    mdy = medianvalues[yaxis]
    
    pathxaxis = hv.Path({'x': [mdx, mdx], 'y':[0, maxy]})
    pathxaxis.opts(color='red', line_width=3)
    pathyaxis = hv.Path({'x': [0, maxx], 'y':[mdy, mdy]}, color='red')
    pathyaxis.opts(color='red', line_width=3)

    return p*pathxaxis*pathyaxis


def generate_scatter_plot_industries(source, xaxis, yaxis, industries="all", exclude_unknowns = 1, overlay=0):   
    '''
    Returns a Holoviews Point Plot showing policy data in a scatter plot format split by industries.

        Parameters:
            source (df): a dataframe with the appropiate data. It assumes it has a URL column and an industries column for each entry.
            xaxis (str): a string showing what the x-axis variable should be.
            yaxis (str): A string indicating what the y-axis variable should be
            industries (list): An optional list of strings of what industries should be plotted. If left to its default value ("all"), the code will create a visualization for each industry present in the dataframe. 
            exclude_unknowns (int): An optional 0/1 flag. The default is 1. If set to 1, the plot will exclude policies of type 'Unknown'. If set to 0, the plot will contain policies of type "Unknown".
            overlay (int): An optional 0/1 flag. The default is 0. If set to 0, the plots will be displayed differently (one separate plot for each industry). If set to 1, the plots will be overlaid one on top of the other.

        Returns:
            q (Points): A Holoviews Points object

    '''
    # Make HoverTool
    hovertool_opts = {"URL": '@url',
                      "Vagueness": '@vague',
                      "Length": '@length',
                      "Industry": '@industry',
                      }
    hover = create_hovertool(hovertool_opts)

    # Make TapTool
    taptool = create_taptool()

    list_of_figures = []

    # Initial Variables (hardcoded for now)
    width = 1000
    height = 1000
    size = 10
    colors=['red', 'blue', 'green', 'grey', 'pink', 'purple', 'black', 'brown', 'yellow', 'orange']
    markers = ['plus', 'circle_x', 'triangle', 'square', 'cross', 'diamond', 'hex', 'star', 'x', 'dot']

    # Get list of industries
    if industries == "all":
        industries = source['industry'].unique()

    # Iterate through all industries and generate a unique plot for each industry
    counter = 0    
    for industry in industries:
        if industry == "Unknown":
            if exclude_unknowns == 1:
                continue 
        subset = source[source["industry"]==industry]
        p = hv.Points(subset, [xaxis, yaxis])
    
        p.opts(width=width, height=height, tools=[hover, taptool], size=size, title=industry, xlim=(0,5000), color=colors[counter], marker=markers[counter])
        counter += 1

        list_of_figures.append(p)

    counter = 0
    # Display each industry as a different plot side by side
    if overlay==0:
        for figure in list_of_figures:
            if counter == 0:
                counter += 1
                q = figure
            else:            
                q = q + figure
    
    # Display all industries in the same plot
    if overlay==1:
        for figure in list_of_figures:
            if counter == 0:
                counter += 1
                q = figure
            else:            
                q = q * figure
    
    return q


def generate_df_from_json(data, industries=0):
    '''
    This function takes in a json object and returns a pandas dataframe. 
    This function assumes the json object is in the form of a dictionary of dictionaries, where each key is the id of a privacy policy, and each value is a dictionary with the metadata of each policy.
    RIght now the values are hardcoded as vague, url, length, readability, and industry as an optional parameter. 

        Parameters:
            data (json): A json object containing a dictionary of dictionaries with privacy policy metadata.
            industries (int): An optional 0/1 flag. If set to 1, it assumes data inclueds industry metadata.
        
        Returns:
            df (Points): A pandas dataframe
    '''
    data_list = []
    # Iterate through dictionaries, combine them into a single dictionary.
    for key in data.keys():
        dict_to_add = {
            "id": key,
            "vague": float(data[key]["vague"]),
            "length": int(data[key]["length"]),
            "url": data[key]["url"],
            "readability": float(data[key]["readability"]),
        }

        if industries == 1:
            dict_to_add["industry"] = data[key]["industry"]

        data_list.append(dict_to_add)
    
    df = pd.DataFrame.from_dict(data_list)
    return df


def main():
    # Generate dataframe from policy data in json format. Assumes a format of nested dictionaries, in the form {"id":{"x":1, "y":2}}.
    filename = "./data/visualization_data_industries.json" 
    with open(filename, 'r') as e:
        data = json.load(e)
    df = generate_df_from_json(data, industries=1)

    # Generate scatterplots 
    p=generate_scatter_plot(df, 'length', 'vague', median=0)
    q=generate_scatter_plot_industries(df, 'length', 'readability', overlay=0)
    
    # Save the plots as HTML files. 
    # Here we use the decimate function to only show a percentage of the points at any given time, reducing overplotting and increasing performance).
    hv.save(decimate(p), "./holoviews_vis/holoviews_length_vague.html")
    hv.save(decimate(q), "./holoviews_vis/holoviews_length_vague_industry.html")

    # Option two to solve overplotting: rasterize (creates a cleaner scatterplot but with no interactivity with the points)
    # hv.save(rasterize(p).opts(height=1250, width=750), "./holoviews_vis/holoviews.html")

    
if __name__ == "__main__":
    main()

