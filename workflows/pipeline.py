import json
from pathlib import Path
from urllib.request import Request, urlopen

import matplotlib
from MapTitles import MapTitles
from matplotlib import pyplot as plt
from ProximityLayer import ProximityLayer
from RadiusArc import RadiusArc
from RailwayLayer import RailwayLayer
from StationLabels import StationLabels

matplotlib.use("Agg")
matplotlib.rcParams["font.family"] = ["Gill Sans", "DejaVu Sans"]


class MapBuilder:
    BOUNDARY_URL = (
        "https://raw.githubusercontent.com/nuuuwan/gig-data/"
        "master/geo/district/LK-11.json"
    )

    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]
        self.stations = self._read_json(self.root / "data/stations.json")

    def _read_json(self, path):
        with path.open(encoding="utf-8") as source:
            return json.load(source)

    def _boundary(self):
        request = Request(
            self.BOUNDARY_URL, headers={"User-Agent": "cmb-rail"}
        )
        with urlopen(request) as response:
            return json.load(response)

    def _station_bounds(self):
        latitudes, longitudes = zip(*self.stations.values())
        return (
            min(longitudes),
            max(longitudes),
            min(latitudes),
            max(latitudes),
        )

    def _add_boundary(self, axes, boundary):
        for ring in boundary:
            longitudes, latitudes = zip(*ring)
            axes.plot(longitudes, latitudes, color="#343434", linewidth=1)

    def _center(self, axes):
        west, east, south, north = self._station_bounds()
        longitude = (west + east) / 2
        latitude = (south + north) / 2
        radius = max(east - west, north - south) * 0.55
        axes.set_xlim(longitude - radius, longitude + radius)
        axes.set_ylim(latitude - radius, latitude + radius)

    def build(self):
        boundary = self._boundary()
        figure, axes = plt.subplots(figsize=(8, 8))
        self._center(axes)
        proximity = ProximityLayer(self.stations)
        proximity.add(axes)
        RadiusArc(self.stations["Colombo Fort"]).add(axes)
        self._add_boundary(axes, boundary)
        railway = RailwayLayer(self.stations)
        paths = sorted((self.root / "data/lines").glob("*.json"))
        railway.add(axes, paths)
        StationLabels(self.stations).add(axes)
        axes.set_aspect("equal")
        axes.set_axis_off()
        proximity.add_legend(axes)
        railway.add_legend(axes)
        MapTitles().add(figure, axes, len(self.stations))
        figure.tight_layout()
        output = self.root / "map.png"
        figure.savefig(output, dpi=300, facecolor="white")
        plt.close(figure)
        return output


if __name__ == "__main__":
    print(MapBuilder().build())
