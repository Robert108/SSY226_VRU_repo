using System;
using System.Collections.Generic;
using System.Text;

namespace VehicleSim.Playback
{
    public class Waypoint : GeoCoordinatePortable.GeoCoordinate
    {
        public int Time { get; set; }

        public double GetHeadingTo(Waypoint other)
        {
            var x = Math.Sin(AsRad(other.Longitude - this.Longitude)) * Math.Cos(AsRad(other.Latitude));
            var y = Math.Cos(AsRad(this.Latitude)) * Math.Sin(AsRad(other.Latitude)) - Math.Sin(AsRad(this.Latitude)) * Math.Cos(AsRad(other.Latitude)) * Math.Cos(AsRad(other.Longitude - this.Longitude));

            return AsHeading(Math.Atan2(x, y));
        }

        private double AsRad(double degrees)
        {
            return degrees * (Math.PI / 180);
        }

        private double AsHeading(double radians)
        {
            return ((radians * 180 / Math.PI) + 360) % 360;
        }
    }
}
