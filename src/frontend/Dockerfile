# Usar la imagen del SDK de .NET 8.0 para compilar el proyecto
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
WORKDIR /app

# Copiar csproj y restaurar dependencias
COPY *.csproj ./
RUN dotnet restore

# Copiar el resto de los archivos y construir
COPY . ./
RUN dotnet publish -c Release -o out

# Generar la imagen final basada en el runtime de .NET 8.0
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build-env /app/out .

# Exponer el puerto 80 en la imagen final
EXPOSE 80

ENTRYPOINT ["dotnet", "DataDiver.dll"]
