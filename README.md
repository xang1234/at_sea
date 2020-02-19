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
It is preferable to use this external data source as port locations instead

<p align="center">
<img  src="img/inferred_ports.png" width="600" height="300" >
</p>


## Modelling 

Insufficient time was spent on modelling so there are more ideas than code

### Time Series





### Graphs 

### Geometry 

