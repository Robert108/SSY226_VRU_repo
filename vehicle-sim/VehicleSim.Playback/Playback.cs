using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace VehicleSim.Playback
{
    public static class Playback
    {
        public static string ScenarioPath { get; set; }

        private static List<Scenario> scenarios;
        public static List<Scenario> Scenarios
        {
            get
            {
                if (scenarios == null)
                {
                    scenarios = LoadScenarios();
                }

                return scenarios;
            }
        }

        private static List<Scenario> LoadScenarios()
        {
            List<Scenario> result = new List<Scenario>();

            foreach (var file in Directory.EnumerateFiles(ScenarioPath))
            {
                string scenarioYaml = File.ReadAllText(file);

                var deserializer = new DeserializerBuilder()
                    .WithNamingConvention(new CamelCaseNamingConvention())
                    .Build();

                var scenario = deserializer.Deserialize<Scenario>(scenarioYaml);

                result.Add(scenario);
            }

            return result;
        }
        public static void Replay(Scenario scenario, Nats nats)
        {
            List<VehiclePosition> timedWaypoints = GetTimedWaypointFromScenario(scenario);

            ReplayTimedWaypoints(nats, timedWaypoints);
        }

        public static void Replay(List<Scenario> scenarios, Nats nats)
        {
            List<VehiclePosition> timedWaypoints = new List<VehiclePosition>();
            foreach (var scenario in scenarios)
            {
                timedWaypoints.AddRange(GetTimedWaypointFromScenario(scenario));
            }

            ReplayTimedWaypoints(nats, timedWaypoints);
        }

        private static List<VehiclePosition> GetTimedWaypointFromScenario(Scenario scenario)
        {
            var timedWaypoints = new List<VehiclePosition>();

            foreach (var vehicleEntry in scenario.Vehicles)
            {
                var vehicle = vehicleEntry.Value;
                vehicle.Id = vehicleEntry.Key;
                vehicle.AsPositionEverySecond().ForEach(position => timedWaypoints.Add(new VehiclePosition() { Vehicle = vehicle, Position = position }));
            }

            return timedWaypoints;
        }

        private static void ReplayTimedWaypoints(Nats nats, List<VehiclePosition> timedWaypoints)
        {
            var timeOrderedWaypoints = timedWaypoints.OrderBy(x => x.Position.Timestamp);

            foreach (var vehiclePosition in timeOrderedWaypoints)
            {
                var now = DateTimeOffset.Now;
                if (now < vehiclePosition.Position.Timestamp)
                {
                    Thread.Sleep((int)vehiclePosition.Position.Timestamp.Subtract(now).TotalMilliseconds);
                }

                var json = JsonSerializer.GetJsonPositionReport(vehiclePosition.Vehicle, vehiclePosition.Position);
                Console.Out.WriteLine(json);
                if (nats != null)
                {
                    nats.Publish("vehicle." + vehiclePosition.Vehicle.Id + ".position", json);
                }
            }
        }
    }


    internal class VehiclePosition
    {
        internal Vehicle Vehicle { get; set; }
        internal GeoCoordinatePortable.GeoPosition<Waypoint> Position { get; set; }
    }
}
