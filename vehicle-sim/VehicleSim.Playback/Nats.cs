using NATS.Client;
using System;
using System.Collections.Generic;
using System.Security;
using System.Text;

namespace VehicleSim.Playback
{
    public class Nats
    {
        public static string Url { private get; set; }
        public static string User { private get; set; }
        public static string Password { private get; set; }

        private IConnection connection;
        private IConnection Connection
        {
            get
            {
                if (connection == null)
                    Connect();

                return connection;
            }
        }

        private void Connect()
        {
            var connectionFactory = new ConnectionFactory();
            var options = ConnectionFactory.GetDefaultOptions();
            options.Url = Url;
            options.User = User;
            options.Password = Password;
            connection = connectionFactory.CreateConnection(options);
        }

        public void Publish(string topic, string data)
        {
            Connection.Publish(topic, Encoding.UTF8.GetBytes(data));
        }

        public void Close()
        {
            if (connection != null)
                Connection.Close();
        }
    }
}
