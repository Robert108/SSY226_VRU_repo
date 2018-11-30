FROM openjdk:8-jre-alpine

COPY mqtt-spy-daemon-1.0.0.jar /app.jar

ENTRYPOINT ["/usr/bin/java", "-jar", "/app.jar", "/config/daemon.xml"]
