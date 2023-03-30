# pivacy-policy-visualizations
Repo showing interactive visualizations for privacy policy data for the Privaseer project.

bokehrandomdata.py --> A python file that contains the code to generate the visualizations. It requires [bokeh](https://bokeh.org/) and [pandas](https://pandas.pydata.org/) to run; please refer to these websites for installation instructions. 

samplerandompolicydata --> a CSV file with randomly generate fake policy points

bokehrandomdata.html --> A standalone html file with the visualization. The output of bokehrandomdata.py

scatterplotdiv.html --> Contains the div html for the scatterplot. It is the output of the [components](https://docs.bokeh.org/en/2.4.3/docs/user_guide/embed.html) function provided by bokeh. 

scatterplotscript.html --> Contains the script html for the scatterplot. It is the output of the [components](https://docs.bokeh.org/en/2.4.3/docs/user_guide/embed.html) function provided by bokeh.

index.html --> A basic html template that will incorporate scatterplotdiv.html and scatterplotscript.html
