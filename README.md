# curious_shop

<b><i>widget.py</i></b>	is a bokeh-based interactive app that plots the Energy Star scores of buildings by paramters such as business type, state, gross square footage, and year constructed. It needs the following files to be in the same directory: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;  <i><b>EnergyStarBuildingsForPlot.csv</i></b>	 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;  <i><b>allStates.txt</i></b>		<br/> 
&nbsp;&nbsp;&nbsp;&nbsp;  <i><b>info.html</i></b>		<br/>
&nbsp;&nbsp;&nbsp;&nbsp;  <i><b>legend.png</i></b>		<br/>

To view, install bokeh and pandas.
```
conda install bokeh
conda install pandas
```

or
```
pip install bokeh
pip install pandas
```

Download the files, navigate to the download directory, then run at command prompt
```
bokeh serve --show widget.py
```

<br/><br/><br/>


<b><i>esbt.html</i></b>	is a folium-based interactive app that plots the Energy Star scores of buildings by their <b>business types</b> and locations. It needs <b><i>esbt.js</i></b> in the same directory.

<b><i>eszcm.html</i></b> is a folium-based interactive app that plots the Energy Star scores of buildings by their <b>zipcodes</b> and locations. It needs <b><i>eszcm.js</i></b>	in the same directory.

