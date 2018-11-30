using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using VehicleSim.Playback;

namespace VehicleSim.Pages
{
    public class IndexModel : PageModel
    {
        public List<Scenario> Scenarios { get; private set; }

        public void OnGet()
        {
            Scenarios = Playback.Playback.Scenarios;

            if(Request.Query.ContainsKey("playback"))
            {
                var scenarioName = Request.Query["playback"];
                var scenario = Scenarios.Where(x => x.Name == scenarioName).First();

                Playback.Playback.Replay(scenario, Startup.Nats);
            }
        }
    }
}
