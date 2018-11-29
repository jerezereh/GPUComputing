Simplifying Taxi Cab Routes
===========================
Note: the source of taxi-cab trajectory data for this project can be found [here](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/?from=https%3A%2F%2Fresearch.microsoft.com%2Fapps%2Fpubs%2F%3Fid%3D152883).

This aim of this project is to calculate simplified taxi routes using parallel GPU computing, which would be able to find the simplest route far quicker than the linear computations of a CPU. The project uses plaintext taxi data, Nvidia's CUDA platform to computer on the GPU, and [Mapbox](https://www.mapbox.com/), a GIS service, to display the results.

The workflow for this project thusfar was done manually: 
1. Convert taxi plaintext data to geojson.
2. Upload resulting geojson to Mapbox for initial taxi route.
3. Create or find a set of points in plaintext that the taxi route cannot simplify out.
4. Use plaintext taxi data and point set in line simplification program.
5. Upload new simplified route to Mapbox.
