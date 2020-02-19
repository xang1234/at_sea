# Predicting Ship Loading at Port 

Due to unfamiliarity with AWS, most of the processing was done using compute on Kaggle.  

## Preprocessing

 Place AWS credentials in ./src/utils/ and run 

~~~
$ sh ./bin/preprocess.sh
~~~

Processing is done using pandas. In order to limit memory usage, data is read and processed by
chunks, this is possible provided processing is done by key and the data is already sorted by same key before hand. 

* **get_data** runs queries on Athena, split by _lrimoshipno_ and ordered by _lrimoshipno_ and _movementdatetime_
* **get_ports** determines port locations. A ship's average speed is calculated and if it is below a certain speed 
(default 0.1 km/h) for a certain amount of time (default 24h), 
it is considered to be in a vicinity of a port 
* **join_ports** combines the outputs of **get_ports** and eliminates duplicates within a certain distance (default 10 km)
* **dbscan_ports** uses clustering as an alternative to eliminating 'duplicate' ports within a certain distance
* **get_endpoints** determines the journey of each ship when it leaves port A and arrives at port B

Based on the analysis, we obtain some 603 ports. Some ports do not appear, this is most obvious around Europe


<p align="center">
<img  src="img/inferred_ports.png" width="600" height="300" >
</p>

Data from [WFPGeoNode](https://geonode.wfp.org/layers/geonode:wld_trs_ports_wfp) has more than 3000 ports available. 
It is preferable to use this external data source as port locations instead. 

<p align="center">
<img  src="img/world_ports.png" width="600" height="300" >
</p>


## Modelling 

Unfortunately, insufficient time was spent on modelling so there are more ideas than code.

~~~
$ sh ./bin/model.sh
~~~

* _features_ determines the nearest WFPGeoNode port for each itinerary (departure and arrival)
*  
*

Based on the pre-processing :
* All ships : 144k trajectories, 13634 ships and 2800 ports
* Ships with dwt >= 150k : 144k trajectories, 1645 ships and 


Location of ports visited by ships with dwt above 150k:
<p align="center">
<img  src="img/heavy_ports.png" width="600" height="300" >
</p>


### Time Series

Since the endpoint data is aggregated and since the prediction period is relatively 
long (14 days), it is tempting to just use time series data to predict the number of ships loading. 

Assuming the pre-processing is correct, this are samples of how arrivals at ports vary over time: 

<p float="center">
  <img src="img/port_hedland.png" width="400" height="300" />
  <img src="img/dampier.png" width="400" height="300" /> 

</p>

if we naively use the 14 day average on 1st Jan 2020 to predict the number of arrivals for 2-15 Jan, we would get an accuracy
of 48% and 91% respectively for Dampier and Port Hedland. 

while the moving average gives a certain approximation, large spikes or dips would be missed. Pure time series methods
do not seem to be of use here to deal with the fluctuations.


### Graphs 
#### Hierarchical Clustering of Ports  

We construct a directed graph with ports as nodes and ship trajectories as edges 
( it is better to use travelled distance instead of straight line distance). A clustering 
 
 the goal being to identify 



### Ship Movement Data 

While ship movement data (location, speed, heading, etc.) can give us more granularity, the relatively long 
forecast period increases uncertainty; 
a ship could head to port A, then port B and then possibly port C within that time frame. 

Some ports are also located close to each other, so a ship could be headed to any one of them. 

<p float="center">
  <img src="img/oz.png" width="400" height="300" />
</p>