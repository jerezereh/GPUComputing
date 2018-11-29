Simplifying Taxi Cab Routes
===========================

This aim of this project is to calculate simplified taxi routes using parallel GPU computing, which would be able to find the simplest route far quicker than the linear computations of a CPU. The project uses plaintext taxi data, Nvidia's CUDA platform to computer on the GPU, and [Mapbox](https://www.mapbox.com/), a GIS service, to display the results.

## Workflow
1. Convert taxi plaintext data to geojson. Use: `python3 ./txtToGeojson.py [directory]`. Directory must contain 1 or more .txt files.
2. Upload resulting geojson to Mapbox for initial taxi route. Done manually through Mapbox's UI.
3. Create or find a set of points in plaintext that the taxi route cannot simplify out. For arbitrary points for testing, use: `python3 ./randomPointsGen.py [geojson file] [number of points to generate]`. GeoJSON file gives latitude and longitude boundaries for new points.
4. Use plaintext taxi data and point set in line simplification program. Use: `python3 ./lineSimplification.py [geojson file] [plaintext coordinates]`. Geojson must contain 1 or more linestrings, which will be simplified to simplest routes that still contain points given in the plaintext coordinates file.
5. Upload new simplified route to Mapbox. Done manually through Mapbox's UI.

## Example GeoJSON file:
`{
 "type": "FeatureCollection",
 "features": [
  {
   "type": "Feature",
   "geometry": {
    "type": "LineString",
    "coordinates": [
     [
      116.45186,
      39.93225
     ],
     [
      116.46777,
      39.93235
     ],
     [
      116.47501,
      39.9323
     ],
     [
      116.4709,
      39.90385
     ]
    ]
   },
   "properties": {
    "id": "10357",
    "r": 230,
    "g": 245,
    "b": 199
   }
  },` ...
  
GeoJSON files are in the standard format, with the id equal to the taxi number, and randomly generated rgb values to differentiate taxis on the map.

## Example plaintext coordinates file:
`116.47602081298827,39.82013946676259`  
`116.44718170166017,39.84887587825816`  
`116.4166259765625,39.90710270565395`   
`116.40220642089842,39.935802707704816`   
...

Coordinates in "longitude,latitude" form, note there is no space between them.

## Resources
This project uses Python v3.6, the Python GeoJSON library available [here](https://github.com/frewsxcv/python-geojson), and the [T-Drive taxi data](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/?from=https%3A%2F%2Fresearch.microsoft.com%2Fapps%2Fpubs%2F%3Fid%3D152883) by Zheng et al.
