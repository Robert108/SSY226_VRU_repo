using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;

namespace VehicleSim.Playback
{
    public static class JsonSerializer
    {
        private static readonly string TEMPLATE = @"{{""time"":""{0}"",""lat"":{1},""lon"":{2},""climb"":{3},""course"":{4},""eps"":{5},""ept"":{6},""epv"":{7},""epx"":{8},""epy"":{9},""speed"":{10},""alt"":{11},""client_version"":{12},""vehicle_type"":""{13}""}}";

        public static string GetJsonPositionReport(Vehicle vehicle, GeoCoordinatePortable.GeoPosition<Waypoint> waypoint)
        {

            var positionReport = new PositionReport()
            {
                client_version = 1.ToString(),
                vehicle_type = vehicle.Type,

                // Real fake numbers
                time = waypoint.Timestamp.ToString("o"),
                lat = waypoint.Location.Latitude.ToString("F6"),
                lon = waypoint.Location.Longitude.ToString("F6"),
                course = waypoint.Location.Course.ToString("F2"),
                speed = waypoint.Location.Speed.ToString("F2"),

                // Hard-coded elsewhere
                alt = waypoint.Location.Altitude.ToString("F2"),
                epx = waypoint.Location.HorizontalAccuracy.ToString("F2"),
                epy = waypoint.Location.VerticalAccuracy.ToString("F2"),

                // Hard-coded here
                climb = 0.0.ToString("F2"),
                eps = 0.0.ToString("F2"),
                ept = 0.0.ToString("F2"),
                epv = 0.0.ToString("F2")
            };

            return String.Format(TEMPLATE,
                positionReport.time,
                positionReport.lat,
                positionReport.lon,
                positionReport.climb,
                positionReport.course,
                positionReport.eps,
                positionReport.ept,
                positionReport.epv,
                positionReport.epx,
                positionReport.epy,
                positionReport.speed,
                positionReport.alt,
                positionReport.client_version,
                positionReport.vehicle_type
               );
        }
    }

    internal class PositionReport
    {
        internal string vehicle_type;
        internal string client_version;
        internal string time;
        internal string lat;
        internal string lon;
        internal string speed;
        internal string course;
        internal string alt;
        internal string climb;
        internal string ept;
        internal string epx;
        internal string epy;
        internal string epv;
        internal string eps;
    }
}
