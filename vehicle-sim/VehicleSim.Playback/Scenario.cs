using System;
using System.Collections.Generic;
using System.Text;

namespace VehicleSim.Playback
{
    public class Scenario
    {
        public string Name { get; set; }
        public string Description { get; set; }

        public Dictionary<string, Vehicle> Vehicles { get; set; }
    }
}
