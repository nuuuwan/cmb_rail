import json
from math import asin, cos, radians, sin, sqrt

from matplotlib.lines import Line2D


class RailwayLayer:
    EARTH_RADIUS_KM = 6371.0
    COLORS = {
        "<1 km": "#9ca3af",
        "1 km to 2 km": "#f9a8d4",
        ">2 km": "#dc2626",
    }

    def __init__(self, stations):
        self.stations = stations

    def _distance(self, first, second):
        first_latitude, first_longitude = map(radians, first)
        second_latitude, second_longitude = map(radians, second)
        latitude_delta = second_latitude - first_latitude
        longitude_delta = second_longitude - first_longitude
        haversine = sin(latitude_delta / 2) ** 2
        haversine += (
            cos(first_latitude)
            * cos(second_latitude)
            * sin(longitude_delta / 2) ** 2
        )
        return 2 * self.EARTH_RADIUS_KM * asin(sqrt(haversine))

    def _color(self, distance):
        if distance > 2:
            return self.COLORS[">2 km"]
        if distance >= 1:
            return self.COLORS["1 km to 2 km"]
        return self.COLORS["<1 km"]

    def _add_route(self, axes, path):
        with path.open(encoding="utf-8") as source:
            names = json.load(source)
        for first_name, second_name in zip(names, names[1:]):
            first = self.stations[first_name]
            second = self.stations[second_name]
            axes.plot(
                [first[1], second[1]],
                [first[0], second[0]],
                color=self._color(self._distance(first, second)),
                linewidth=4,
                zorder=2,
            )

    def add(self, axes, paths):
        for path in paths:
            self._add_route(axes, path)
        latitudes, longitudes = zip(*self.stations.values())
        axes.scatter(
            longitudes,
            latitudes,
            s=100,
            facecolor="white",
            edgecolor="black",
            linewidth=2,
            zorder=3,
        )

    def add_legend(self, axes):
        handles = [
            Line2D([], [], color=color, linewidth=4, label=label)
            for label, color in self.COLORS.items()
        ]
        axes.legend(
            handles=handles,
            title="Gap between stations",
            frameon=True,
            facecolor="white",
            edgecolor="white",
            framealpha=1,
            loc="upper right",
            bbox_to_anchor=(1, 0.78),
            prop={"family": "Gill Sans", "size": 11},
            title_fontproperties={"family": "Gill Sans", "size": 12},
        )
