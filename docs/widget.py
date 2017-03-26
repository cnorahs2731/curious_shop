#from os.path import dirname, join

import numpy as np
import pandas as pd
#import seaborn as sns

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, Div, HBox, VBox
from bokeh.models.widgets import Slider, Select, TextInput, MultiSelect
from bokeh.io import curdoc, output_file, save
from bokeh.models import NumeralTickFormatter
from bokeh.resources import CDN
from bokeh.embed import file_html, components


#output_file("widget.html", mode="inline")

allData = pd.read_csv('EnergyStarBuildingsForPlot.csv', encoding = "ISO-8859-1", dtype={
    'FacilityName': str,	
    'LabelYears': np.float32,
    'Owner': str,
    'PropertyManager': str,	
    'BuildingSubtype':	str,
    'BuildingType': str,	
    'City':	 str,
    'State': str,	
    'StateCode': str,	
    'Zip':	str,
    'Scores': np.float32,	
    'GSF':	np.float64,
    'YearConstructed': np.float32,
    'dotSize': np.float32,	
    'alpha': np.float32,
    'dotColor': str,
    'lineColor': str,
    'lineWidth': np.float32,
    'lineAlpha': np.float32,
    })

axis_map = {
    "Label Years": "LabelYears",
    "Scores": "Scores",
    "GSF": "GSF",
    "Year Constructed": "YearConstructed",
}

desc = Div(text=open("info.html").read(), width=1500)

# Create Input controls
label_year_min = Slider(title="Label Year (earliest)", value=2005, start=1999, end=2016, step=1,)
label_year_max = Slider(title="Label Year (latest)", value=2016, start=1999, end=2016, step=1,)
score_min = Slider(title="Score (at least)", start=75, end=100, value=80, step=1,)
score_max = Slider(title="Score (at most)", start=75, end=100, value=95, step=1,)
gsf_min = Slider(title="Gross Square Footage in kft^2, (at least)", start=0, end=9000, value=0, step=10,)
gsf_max = Slider(title="Gross Square Footage in kft^2, (at most)", start=0, end=9000, value=150, step=10,)
year_constr_min = Slider(title="Year Constructed (after)", start=1820, end=2015, value=1980, step=1,)
year_constr_max = Slider(title="Year Constructed (before)", start=1820, end=2015, value=2015, step=1,)
state = MultiSelect(title="State", value=["California"],
        options=open('allStates.txt').read().split('\n'),)
bldgType = MultiSelect(title="Type", value=['BANKING','EDUCATION','FOOD_SALES_SERVICE',
    'HEALTHCARE','LODGING_RESIDENTIAL','MISC','MIXED_USE','OFFICE','PUBLIC_SERVICES',
    'RELIGIOUS_WORSHIP','RETAIL','WAREHOUSE_STORAGE',],
    options=open('allBldgTypes.txt').read().split('\n'),)
zipcode = TextInput(title="Zipcode",)

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="GSF",)
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Scores",)


# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], dotSize=[], dotColor=[], alpha=[],
                                    lineColor=[], lineWidth=[], lineAlpha=[],
                                    facilityName=[], owner=[], propertyMgr=[], 
                                    bldgType=[], bldgSubtype=[], 
                                    city=[], zipcode=[], state=[], gsf=[], score=[]))

hover = HoverTool(tooltips=[
    ("Name", "@facilityName"),
    ("Owner", "@owner"),
    ("Score", "@score"),
    ("Type", "@bldgSubtype"),
    ("City", "@city"),
    ("State", "@state"),
    ("Zip", "@zipcode"),
    ("GSF", "@gsf"+" sq ft"),      
])

p = figure(plot_height=800, plot_width=700, title="", toolbar_location="above", 
           tools=[hover,BoxZoomTool(),ResetTool()])
p.circle(x="x", y="y", source=source, size="dotSize", color="dotColor", 
         line_color="lineColor", line_width="lineWidth", fill_alpha="alpha")
p.axis.axis_label_text_font_style = "bold"
p.axis.major_label_text_font_style = "bold"
p.axis.axis_label_text_font_size = "16pt"
p.axis.major_label_text_font_size = "14pt"
p.xaxis.formatter = NumeralTickFormatter(format="0")
p.yaxis.formatter = NumeralTickFormatter(format="0")
p.title.text_font_size = "16pt"

html = file_html(p, CDN, "my plot")
handle = open("filename.html","w")
handle.write(html)
handle.close


# 6 different line colors, 3 different line widths, 3 different line dashes
#line_color
#line_width
#line_dash

def select_data():
    bldgType_val = bldgType.value
    state_val = state.value
    zip_val = str(zipcode.value).strip()
    selected = allData[
        (allData.LabelYears >= label_year_min.value) &
        (allData.LabelYears <= label_year_max.value) &
        (allData.Scores >= score_min.value) &
        (allData.Scores <= score_max.value) &
        (allData.GSF >= (gsf_min.value * 1e3)) &
        (allData.GSF <= (gsf_max.value * 1e3)) &
        (allData.YearConstructed >= year_constr_min.value) &
        (allData.YearConstructed <= year_constr_max.value)        
    ]
    selected = selected[selected['BuildingType'].isin(bldgType_val)] 
    selected = selected[selected['State'].isin(state_val)] 
    if (zip_val != ""):
        selected = selected[selected.Zip.str.contains(zip_val)==True]
    return selected


def update():
    df = select_data()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]
    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "%d buildings, %d scores selected" % (len(df["FacilityName"].unique()), len(df))
    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        dotSize=df["dotSize"],
        dotColor=df["dotColor"],
        alpha=df["alpha"],
        lineColor=df["lineColor"], 
        lineWidth=df["lineWidth"], 
        lineAlpha=df["lineAlpha"],
        facilityName=df["FacilityName"],
        owner=df["Owner"],
        propertyMgr=df["PropertyManager"],
        bldgType=df["BuildingType"], 
        bldgSubtype=df["BuildingSubtype"], 
        city=df["City"], 
        zipcode=df["Zip"], 
        state=df["State"],
        gsf=df["GSF"],
        score=df["Scores"],
    )


controls = [x_axis, y_axis, score_min, score_max, 
            bldgType, gsf_min, gsf_max, 
            state, zipcode, label_year_min, label_year_max, 
            year_constr_min, year_constr_max]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'scale_width'  # 'fixed', or 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)

l = layout([
    [desc], # PUT A LEGEND HERE
    [inputs, p],
    ], sizing_mode=sizing_mode)


update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Interactive Energy Star Scores"







