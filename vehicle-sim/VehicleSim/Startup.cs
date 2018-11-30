using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace VehicleSim
{
    public class Startup
    {
        public static IHostingEnvironment HostingEnvironment { get; private set; }
        public static Playback.Nats Nats { get; private set; }
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseBrowserLink();
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
            }

            app.UseStaticFiles();

            app.UseMvc();

            Playback.Playback.ScenarioPath = Path.Combine(env.WebRootPath, "scenarios");
            Playback.Nats.Url = Environment.GetEnvironmentVariable("NATS_URL");
            Playback.Nats.User = Environment.GetEnvironmentVariable("NATS_USER");
            Playback.Nats.Password = Environment.GetEnvironmentVariable("NATS_PASS");
            Nats = new Playback.Nats();

            HostingEnvironment = env;
        }
    }
}
