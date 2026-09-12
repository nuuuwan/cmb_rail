import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


class ProximityLayer:
    EARTH_RADIUS_KM = 6371.0
    COLORS = ["#4caf50", "#facc15", "#f97316"]
    LABELS = ["<500 m", "500 m to 1 km", "1 km to 2 km"]

    def __init__(self, stations):
        self.stations = np.radians(np.array(list(stations.values())))

    def _nearest_distances(self, latitudes, longitudes):
        latitude_radians = np.radians(latitudes)
        longitude_radians = np.radians(longitudes)
        nearest = np.full(latitudes.shape, np.inf)
        for station_latitude, station_longitude in self.stations:
            latitude_delta = latitude_radians - station_latitude
            longitude_delta = longitude_radians - station_longitude
            haversine = np.sin(latitude_delta / 2) ** 2
            haversine += (
                np.cos(latitude_radians)
                * np.cos(station_latitude)
                * np.sin(longitude_delta / 2) ** 2
            )
            distance = 2 * self.EARTH_RADIUS_KM * np.arcsin(np.sqrt(haversine))
            nearest = np.minimum(nearest, distance)
        return nearest

    def add(self, axes):
        west, east = axes.get_xlim()
        south, north = axes.get_ylim()
        longitude_values = np.linspace(west, east, 500)
        latitude_values = np.linspace(south, north, 500)
        longitudes, latitudes = np.meshgrid(longitude_values, latitude_values)
        distances = self._nearest_distances(latitudes, longitudes)
        classes = np.select(
            [distances < 0.5, distances <= 1, distances <= 2],
            [0, 1, 2],
            default=np.nan,
        )
        axes.pcolormesh(
            longitudes,
            latitudes,
            classes,
            cmap=ListedColormap(self.COLORS),
            vmin=0,
            vmax=2,
            alpha=0.25,
            shading="auto",
            zorder=0,
        )

    def add_legend(self, axes):
        handles = [
            Patch(facecolor=color, alpha=0.25, label=label)
            for color, label in zip(self.COLORS, self.LABELS)
        ]
        legend = axes.legend(
            handles=handles,
            title="Distance to station",
            frameon=True,
            facecolor="white",
            edgecolor="white",
            framealpha=1,
            loc="upper right",
            prop={"family": "Gill Sans", "size": 11},
            title_fontproperties={"family": "Gill Sans", "size": 12},
        )
        axes.add_artist(legend)
