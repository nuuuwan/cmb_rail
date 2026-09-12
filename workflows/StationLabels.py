class StationLabels:
    def __init__(self, stations):
        self.stations = stations

    def add(self, axes):
        for name, (latitude, longitude) in self.stations.items():
            axes.annotate(
                name,
                (longitude, latitude),
                xytext=(5, 3),
                textcoords="offset points",
                fontsize=6.5,
                color="black",
                zorder=3,
            )
