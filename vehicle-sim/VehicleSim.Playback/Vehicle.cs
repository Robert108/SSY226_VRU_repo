using System;
using System.Collections.Generic;
using System.Text;

namespace VehicleSim.Playback
{
    public class Vehicle
    {
        public string Id { get; set; }
        public string Type { get; set; }
        public List<Waypoint> Route { get; set; }

        public List<GeoCoordinatePortable.GeoPosition<Waypoint>> AsPositionEverySecond()
        {
            var result = new List<GeoCoordinatePortable.GeoPosition<Waypoint>>();
            var startTime = DateTime.UtcNow;
            var secondOffset = 0;

            for (int index = 0; index < Route.Count - 1; index++)
            {
                var current = Route[index];
                var next = Route[index + 1];

                var distance = current.GetDistanceTo(next);
                var duration = next.Time - current.Time;
                var speed = distance / duration;
                var heading = current.GetHeadingTo(next);
                var latitudePerSecond = (next.Latitude - current.Latitude) / duration;
                var longitudePerSecond = (next.Longitude - current.Longitude) / duration;

                for(int step = 0; step <= duration; step ++)
                {
                    var waypoint = new Waypoint()
                    {
                        Time = secondOffset,
                        Latitude = current.Latitude + step * latitudePerSecond,
                        Longitude = current.Longitude + step * longitudePerSecond,
                        Speed = speed,
                        Course = heading,
                        Altitude = 2,
                        HorizontalAccuracy = 1.0,
                        VerticalAccuracy = 1.0
                    };
                    DateTimeOffset time = startTime.AddSeconds(secondOffset);

                    var position = new GeoCoordinatePortable.GeoPosition<Waypoint>()
                    {
                        Location = waypoint,
                        Timestamp = time
                    };

                    result.Add(position);

                    secondOffset += 1;
                }
                
            }

            return result;
        }
    }
}
