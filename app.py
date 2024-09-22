import asyncio
import mtrpacket
import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=['POST'])
def get_ip():
    domain = request.json['domain']
    # print(domain)
    route = []

    myip = str(requests.get('https://ipecho.net/plain').text)
    route.append(lookup_ip(myip))

    routes = tracer(domain)
    hops = route + routes

    geo = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": {
            "type": "LineString",
            "coordinates": []
        },
            "properties": {
            "name": "route"
        }
        }
        ]
    }

    for hop in hops:
        # print(hop)
        feature = {"type": "Feature", "geometry": {
            "type": "Point",
            "coordinates": [float(hop["lng"]), float(hop["lat"])]
        },
            "properties": {
                "ip": hop["ip"],
                "country": hop["country"]
        }
        }
        geo["features"][0]["geometry"]["coordinates"].append(
            feature["geometry"]["coordinates"])
        geo["features"].append(feature)

    geojson = json.dumps(geo)

    # return render_template("index.html", route=hops, geojson=geojson)
    return geojson


def tracer(domain):
    routes = []

    async def trace():
        async with mtrpacket.MtrPacket() as mtr:
            for ttl in range(1, 256):
                result = await mtr.probe(domain, ttl=ttl)
                # print(result)

                if result.result == "ttl-expired" or result.result == "reply":
                    ip = result.responder

                    # print(f"looking for {ip}")

                    if ip:
                        res = lookup_ip(ip)
                        if res:
                            routes.append(lookup_ip(ip))

                if result.success or result.result == "no-reply":
                    break

    asyncio.new_event_loop().run_until_complete(trace())

    return routes


def lookup_ip(ip):
    if ip:

        url = "https://ipinfo.io/"+ip+"?token=0a8e8b22f38f42"
        # print(url)
        ip_lookup = requests.get(url=url)
        data = ip_lookup.json()
        # print(f"-> { data }")
        if data["ip"]:
            if "bogon" in data:
                return False
            # print("IP: %s country: %s lat: %s, lng: %s" %
            #      (ip, data["country"], data["latitude"], data["longitude"]))
            location = data["loc"].split(",")
            details = {
                "ip": ip,
                "country": data["country"],
                "lat": location[0],
                "lng": location[1]
            }

            return details

        else:
            # print(data["message"])
            return False

    else:
        return ("No IP")


# main().
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
