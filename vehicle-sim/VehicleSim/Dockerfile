FROM microsoft/aspnetcore:2.0 AS base
WORKDIR /app
EXPOSE 80

FROM microsoft/aspnetcore-build:2.0 AS build
WORKDIR /src
COPY VehicleSim/VehicleSim.csproj VehicleSim/
RUN dotnet restore VehicleSim/VehicleSim.csproj
COPY . .
WORKDIR /src/VehicleSim
RUN dotnet build VehicleSim.csproj -c Release -o /app

FROM build AS publish
RUN dotnet publish VehicleSim.csproj -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "VehicleSim.dll"]
