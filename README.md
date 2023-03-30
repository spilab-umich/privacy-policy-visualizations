# pivacy-policy-visualizations
Repo showing interactive visualizations for privacy policy data for the Privaseer project.

bokehJSCDN.html --> Contains the necessary scripts to load BokehJS into an html page. You would add this to the <body></body> tags in your html file to include the scatterplot.

bokehrandomdata.py --> A python file that contains the code to generate the visualizations. It requires [bokeh](https://bokeh.org/) and [pandas](https://pandas.pydata.org/) to run; please refer to these websites for installation instructions. 

samplerandompolicydata --> a CSV file with randomly generated fake policy data.

bokehrandomdata.html --> A standalone html file with the visualization. The output of bokehrandomdata.py.

scatterplotdiv.html --> Contains the div html for the scatterplot. It is the output of the [components](https://docs.bokeh.org/en/2.4.3/docs/user_guide/embed.html) function provided by bokeh. You would add this to the <body></body> tags in your html file to include the scatterplot.

scatterplotscript.html --> Contains the script html for the scatterplot. It is the output of the [components](https://docs.bokeh.org/en/2.4.3/docs/user_guide/embed.html) function provided by bokeh. You would add this to the <head></head> tags in your html file to include the scatterplot.

index.html --> A basic html template that shows how to incorporate the contents of bokehJSCDN.html, scatterplotdiv.html and scatterplotscript.html so as to show the scatterplot in your page. 
