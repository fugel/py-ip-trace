# py-ip-trace

#### Video Demo: [CS50: py-ip-trace](https://youtu.be/D9mMqd29v20)

#### Description:

A web app written in python and Jinga2 templates.

The app takes a domain name such as "bbc.co.uk", then uses mtrpacket to get the hops in a traceroute between your IP address and that of the server hosting the site queried. 

Then using an online api to get the locations of each IP address it draws a pseudo route your web traffic would take to reach that server.

#### Tools

For the backend I chose to use Python, I had a little experience using Pyhton but CS50 really gave me the confidence to use it more.

To ge the IP addresses of the user and the server I used ipecho.net and ipinfo.io which has a free api that allows you to query an IP address. Part of the returned data is a guesstimate of the IPs location in Latitude and Longitude.

I used mtrpacket as the traceroute tool, which is available as a Python package. I then iterate through each IP address mtrpacket returned passing it to the ipinfo.io api and saving the location data in a list.

The list was then passed to a map rendering engine called Map Libre to display the locations as points on a map. I also create a linestring geojson object that is rendered as a line to show the path.

#### Problems

The mtrpacket tool is only available in linux, while this was not initially a problem. I wanted to demonstrate the tool to a collegue at work to get some feedback. However when I tried to run the application in a Windows environment, the mtrpacket tool dependancy was not available.

This made me investigate other ways of running my application, which led me to Docker and creating a Docker container to run my application.
