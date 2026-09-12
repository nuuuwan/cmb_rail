from math import asin, atan2, cos, degrees, radians, sin


class RadiusArc:
    EARTH_RADIUS_KM = 6371.0
    RADIUS_KM = 15.0

    def __init__(self, center):
        self.latitude, self.longitude = map(radians, center)

    def _point(self, bearing):
        bearing = radians(bearing)
        distance = self.RADIUS_KM / self.EARTH_RADIUS_KM
        latitude = asin(
            sin(self.latitude) * cos(distance)
            + cos(self.latitude) * sin(distance) * cos(bearing)
        )
        longitude = self.longitude + atan2(
            sin(bearing) * sin(distance) * cos(self.latitude),
            cos(distance) - sin(self.latitude) * sin(latitude),
        )
        return degrees(latitude), degrees(longitude)

    def add(self, axes):
        latitudes, longitudes = zip(
            *(self._point(bearing) for bearing in range(181))
        )
        axes.plot(
            longitudes,
            latitudes,
            color="#4b5563",
            linewidth=1.5,
            linestyle=(0, (4, 4)),
            zorder=1,
        )
