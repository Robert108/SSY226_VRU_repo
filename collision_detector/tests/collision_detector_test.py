import unittest
import sys
print(sys.path)
from dencity_bike.model.position import Position
from projected_position import ProjectedPosition
from collision_detector import CollisionDetector
from vehicle import Vehicle
from haversine import haversine
import sys
from projectors.vehicle_projector import VehiclePositionProjector
from projectors.human_projector import PersonPositionProjector

class TestStringMethods(unittest.TestCase):

    def setUp(self) :
        self._bus_position = Position()
        self._bus_position.lat = 57.709548
        self._bus_position.lon = 11.941056
        self._bus_position.course  = 44
        self._bus_position.speed = 12.5

        self._bike_position = Position()
        self._bike_position.lat = 57.709627
        self._bike_position.lon = 11.942357
        self._bike_position.course = 338
        self._bike_position.speed = 14.5

        self._human_position = Position()
        self._human_position.lat = 57.709627
        self._human_position.lon = 11.942357
        self._human_position.course = 338
        self._human_position.speed = 7.0

        self._crossing = Position()
        self._crossing.lat = 57.710078
        self._crossing.lon =  11.942016


    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.islower())

    def test_initialization(self):
        bus = Vehicle(Position(), "bus1")
        bike = Vehicle(Position(), "bike1")
        self.assertEqual(bus.id, "bus1")
        self.assertEqual(bike.id, "bike1")

        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        cd.add_to_group_B(bike)
        cd.add_to_group_A(bus)
        self.assertEqual(bike, cd.group_B["bike1"])
        self.assertEqual(bus, cd.group_A["bus1"])

    def test_convert_position_to_coordinate_sw_equals_to_0_0(self):
        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        sw = Position()
        sw.lat = cd.sw[0]
        sw.lon = cd.sw[1]
        self.assertEqual(cd.position_to_coordinate(sw), (0,0))

    def test_convert_position_to_coordinate_ne_equals_to_distance(self):
        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        ne = Position()
        ne.lat = cd._ne[0]
        ne.lon = cd.ne[1]
        self.assertEqual(cd.position_to_coordinate(ne), (round(cd._distance_between_sw_and_se), round(cd._distance_between_sw_and_nw)))

    def test_position_coordinate_inversion(self):
        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        coordinate = cd.position_to_coordinate(self._bus_position)
        convertedPosition = cd.coordinate_to_position(coordinate)
        self.assertEqual((round(self._bus_position.lat, 4), round(self._bus_position.lon, 4)), (round(convertedPosition.lat, 4), round(convertedPosition.lon, 4)))

    def test_projected_position(self):
        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        cp = VehiclePositionProjector()

        projected_bike_position =  cp.projected_position(5, 30, cd.position_to_coordinate, self._bike_position)
        print(projected_bike_position.polygon.exterior.coords)
        bike_exterior_positions = map(cd.coordinate_to_position, projected_bike_position.polygon.exterior.coords)

        print("Bike's projected position")
        for pos in bike_exterior_positions:
            print("{" + "lat: {0}, lng: {1}".format(pos.lat, pos.lon) + "},")

        projected_bus_position =  cp.projected_position(5, 315, cd.position_to_coordinate, self._bus_position)
        bus_exterior_positions = map(cd.coordinate_to_position, projected_bus_position.polygon.exterior.coords)
        print("Bus's projected position")
        for pos in bus_exterior_positions:
            print("{" + "lat: {0}, lng: {1}".format(pos.lat, pos.lon) + "},")

        self.assertFalse(projected_bus_position.intersects(projected_bike_position))

    def test_projected_position_human(self):
        cd = CollisionDetector(logger_handler=sys.stdout, send_warning_callback=None, send_intersection_info_callback=None, deltatime=None)
        human_position_projector = PersonPositionProjector()
        vehicle_position_projector = VehiclePositionProjector()

        projected_human_position =  human_position_projector.projected_position(5, 30, cd.position_to_coordinate, self._human_position)
        print(projected_human_position.polygon.exterior.coords)
        human_exterior_positions = map(cd.coordinate_to_position, projected_human_position.polygon.exterior.coords)

        print("Human's projected position")
        for pos in human_exterior_positions:
            print("{" + "lat: {0}, lng: {1}".format(pos.lat, pos.lon) + "},")

        projected_bus_position =  vehicle_position_projector.projected_position(5, 315, cd.position_to_coordinate, self._bus_position)
        bus_exterior_positions = map(cd.coordinate_to_position, projected_bus_position.polygon.exterior.coords)
        print("Bus's projected position")
        for pos in bus_exterior_positions:
            print("{" + "lat: {0}, lng: {1}".format(pos.lat, pos.lon) + "},")

        self.assertFalse(projected_bus_position.intersects(projected_human_position))

    def test_distance_between_positions(self):
        print(haversine((self._bike_position.lat,self._bike_position.lon), (self._bus_position.lat, self._bus_position.lon)))
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
