# Imagen base del SDK de .NET Core para compilar el proyecto
FROM mcr.microsoft.com/dotnet/sdk:8.0.203 AS build-env
WORKDIR /app

# Copiar csproj y restaurar como una capa distinta para aprovechar la caché de Docker
COPY *.csproj ./
RUN dotnet restore

# Copiar todo lo demás y construir
COPY . ./
RUN dotnet publish -c Release -o out

# Generar la imagen final basada en el runtime de .NET Core
FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "DataDiver.dll"]
