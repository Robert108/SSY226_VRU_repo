using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading;
using VehicleSim.Playback;

namespace VehicleSim.Cli
{
    class Program
    {
        static void Main(string[] args)
        {
            Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US");

            var nats = new Nats();
            Nats.Url = System.Environment.GetEnvironmentVariable("NATS_URL");
            Nats.User = System.Environment.GetEnvironmentVariable("NATS_USER");
            Nats.Password = System.Environment.GetEnvironmentVariable("NATS_PASS");


            var scenarioNames = args;
            Playback.Playback.ScenarioPath = "scenarios";
            var scenarios = Playback.Playback.Scenarios.Where(x => scenarioNames.Contains(x.Name)).ToList();

            Playback.Playback.Replay(scenarios, nats);

            nats.Close();
        }
    }
}
