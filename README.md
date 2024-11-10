# py-ip-trace

#### Video Demo: [CS50: py-ip-trace](https://youtu.be/D9mMqd29v20)

#### Description:

A web app written in python and Jinga2 templates that shows a pseudo route between the web client and server. The locations are estimated using an online api from ipinfo.io which provides a latitude and longitude among other information for the given IP address.

The after the user enters a domain name, app first gathers the client IP address using a different api; ipecho.net, where querying the URL https://ipecho.net/plain gives the users Wide Area Network IP address, this is used as the first IP address in the route.

The application then takes a domain name such as "bbc.co.uk" and uses mtrpacket in a for loop to evaluate each of the hops in the traceroute between the client IP address and that of the server hosting the site queried.

As part of the for loop the api at https://ipinfo.io is queried for each IP address to return the latitude and longitude. This is then used to create a geojson object that contains two types of object; points and linestrings. This are used to denote geographical points on a map for each of the reported IP addresses. The linestring is used to connect the dots and show the “route” the map.

The view is generated using plain HTML and JavaScript, into which a WebGL map is created and loaded along with the minimal controls to submit a URL. The map utilises Maplibre-GL, an opensource JavaScript library for providing interactive, customizable and dynamic maps with advanced features. This takes the geojson generated as part of the above for loop and updates the view to show the locations and route once the user has submitted the URL.

#### Tools

For the backend I chose to use Python, I had a little experience using Python but CS50 really gave me the confidence to use it more.

To ge the IP addresses of the user and the server I used ipecho.net and ipinfo.io which has a free api that allows you to query an IP address. Part of the returned data is a guesstimate of the IPs location in Latitude and Longitude.

I used mtrpacket as the traceroute tool, which is available as a Python package. I then iterate through each IP address mtrpacket returned passing it to the ipinfo.io api and saving the location data in a list.

The list was then passed to a map rendering engine called Map Libre to display the locations as points on a map. I also create a linestring geojson object that is rendered as a line to show the path.

#### Problems

The mtrpacket tool is only available in linux, while this was not initially a problem. I wanted to demonstrate the tool to a collegue at work to get some feedback. However when I tried to run the application in a Windows environment, the mtrpacket tool dependancy was not available.

This made me investigate other ways of running my application, which led me to Docker and creating a Docker container to run my application.