# pivacy-policy-visualizations


# Introduction
This github repo contains the necessary files to create interactive visualizations for privacy policy data for the Privaseer project.

**Current state**: Currently, the code can create very basic scatter plots plotting two variables (e.g., 'vagueness' on the y-axis and policy length on the x-axis) and writes them out as standalone HTML files. In the scatterplots, each privacy policy is represented as one dot on that scatter plot. One can hover over the scatter plot to learn more details about the privacy policy, as well as click on the dot to visit the URL associated with that policy.

**Next Steps** In the short term, we expect to add filtering functionality to scatter plots (for example, a user is able to select from a drop-down menu what industries of privacy policies they want to see.) Long term, there are several goals in mind, including:

* Creating more varied visualizations (e.g., bar charts)
* Improving the look, design, and feel of the visualizations
* Integrating the visualizations into the Privaseer website (more information on how to do this can be found [here](https://holoviews.org/user_guide/Deploying_Bokeh_Apps.html))



# Setup

## Python
This code runs using Python 3.10. To install Python, please follow the instructions on [this website](https://www.python.org/downloads/release/python-3100/)

## Python packages
In addition to Python 3.10, this code makes use of the following packages: [holoviews](https://holoviews.org/), [bokeh](https://bokeh.org/), and [pandas](https://pandas.pydata.org/). Instructions on how to install these packages can be found on their respective websites: having said that, all of these packages are available through [pip](https://pip.pypa.io/en/stable/installation/), and so can be installed using the following commands:

> \> `pip install pandas`

> \> `pip install bokeh`

> \> `pip install holoviews`

## Additional data files
In addition, you will need data that contains the actual privacy policy data from Privaseer. I would have included the data in this github repository, but GitHub has a 100MB storage limit, and the privaseer policy data is much larger than that.

The data must be a json file containing Privaseer policy data in a dictionary of dictionaries format, similar to the following:

    {
        "58a055e3eb7477a963582952132965037ace7057": {
            "vague": "0.1506849315068493",
            "length": 1565,
            "url": "https://ithacaads.com/about-us/14042-privacy-policy",
            "readability": 14.0,
            "industry": "Unknown"
        },
        "2482f5b39109e0000b48a752937ac04150dedf9a": {
            "vague": "0.047619047619047616",
            "length": 463,
            "url": "https://legacyconsultinggroup.com/privacy-statement/",
            "readability": 13.5,
            "industry": "finance, marketing & human resources"
        },
    ...
    }

# Running the code
To run the code, make sure that you have the data file from privaseer and `holoviewsscatterplotgenerator.py`. 

Open `holoviewsscatterplotgenerator.py` and edit the `filename` variable in the `main` function (line 240) to point to your data file (for example, if your privacy policy data is in a file `data.json`, change line 221 in `holoviewsscatterplotgenerator.py` to read `filename = 'data.json'`)

Using your terminal of choice, navigate into the directory where these files are located. Once there, run:

> \> `python holoviewsscatterplotgenerator.py`

After running this command, `holoviewsscatterplotgenerator.py` will read in the data from your data file and create two scatterplots, saving them in the directory `./holoviews_vis/` as `holoviews_length_vague.html` and `holoviews_length_vague_industry.html`. 

# Overview of Files

`holoviewsscatterplotgenerator.py` --> A python file that contains the code to generate the scatter plots. 

`holoviews_vis` --> A folder containing example visualizations generated by `holoviewsscatterplootgenerator.py`