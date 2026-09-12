class MapTitles:
    def add(self, figure, axes, station_count):
        figure.suptitle(
            "Distance to a Railway Station",
            fontsize=24,
            y=0.98,
        )
        axes.set_title(
            f"{station_count} Railway Stations are within 15km "
            "of Colombo Fort.",
            fontsize=13,
            pad=10,
        )
