Notes:
- dataLevels are the indices of the subset of "tesPressureLevels" over which the raw data have been truncated. This omits data outside the range where the retrieval has some sensitivity, and reduces the file size
- avgKernelLevels are the indices of the subset of "tesPressureLevels" over which the averaging kernels have been truncated, for similar reasons
- latIndices and lonIndices are specific to the GISS ModelE2 F40 2x2.5 grid
- dayTimeFlag ==1 for day time observations
- landSurfaceType : -99 for ocn, values from 0-100 for other types defined on p63 of https://eosweb.larc.nasa.gov/PRODOCS/tes/DPS/TES_DPS_V12.0.pdf
- suggest excluding retrievals with HDODegFr < 1 and HDOSpeciesQuality == 0

