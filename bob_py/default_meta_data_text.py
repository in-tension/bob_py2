default_meta_data = """##  any line starting with a # is a comment and is not processed by the code
##
##  all terms in "quotes" are case sensitive and all start with a capital
##  roi_set = "Cell", "Nuc" or "Vor"
##      refers to the ROIs(selections) defining the cells, nuclei, and voronoi respectively
##  intens_im = intensity image
##      an image to gather intensity data from
##      usually a projection of a channel
##      an intens_im is either:
##          read from a tif file in each hemisegment
##              its name comes from the file_name:  hseg-name_IntensImName.tif
##          automatically generated given some parameters
##              its name is defined in this file
##      the name of the intens_im is e
##  msr_param = Measurement Paramaeter
##      one of the output columns from Fiji
##      such as "Area", "X", "Y", "Mean", or "IntDen"
##  calc_func = "Avg", "Tot", or "Norm"
##      average, total, or normalize
##      a function that can be applied to column of nuc data
##          average and total produce values that apply to a cell
##          while normalize produces values for each nucleus
##  prj_method = "avg", "min", "max", "sum", "sd", "median"
##      projection method
##      method used when making a z-projection
##
## <angle-brackets> around a term mean that term is optional

## To Measure: Geometric Parameters
## roi_sets to measure the geometric parameters of
to_msr_geo = [
    "Cell",
    "Vor",
    "Nuc",
]

## To Measure: Intensity Parameters
## for each intens_im, roi_sets to measure the intensity parameters of
## "IntensImName" : ["RoiSetName", "RoiSetName"]
##
to_msr_intens = {
    "Hoe" : ["Nuc"],
    "Fib" : ["Nuc", "Cell"]
}

## To Summarize
## columns to calculate summary stats for - average, total, or norm
## ["RoiSet", <"IntensIm">, "MsrParam"]
to_summarize = [
    ["Vor", "Area"],
    ["Nuc", "Area"],
    ## ["Nuc", "NND"],
    ## ["Nuc", "Hoe", "Ploidy"],
    ["Nuc", "Hoe", "Mean"],
    ["Nuc", "Hoe", "IntDen"],
    ["Nuc", "H3K9ac", "IntDen"],

    ["Nuc", "Fib", "Mean"],
    ["Nuc", "Fib", "IntDen"]]





## Intensity Images to Create
##      intens_im that bob_py should autogenerate
##      a z-projection of a channel
## optional, but if used, requires hseg_slices
## "IntensImName" : (num, "prjmethod")
intens_im_to_create = {
    # "Hoe" : (4, "sum"),
}

## Hemisegment Slices
##      the start and end z-slices for each hemisegment
## "Hemisegment-Name" : [start, end]
hseg_slices = {
    "L1-L1": [1,13],
    "L1-L2": [1,12],
    "L1-L3": [1,13],
    "L1-R1": [1,13],
    "L1-R2": [1,12],
    "L1-R4": [1,12],
    "L2-L1": [1,18],
    "L2-L2": [1,15],
    "L2-L3": [1,15],
    "L2-R1": [1,14],
    "L2-R3": [1,15],
    "L3-L1": [1,13],
    "L3-L2": [1,13],
    "L3-L3": [1,15],
    "L3-R1": [1,13],
    "L3-R2": [1,13],
    "L3-R3": [1,12],
    "L4-L1": [1,17],
    "L4-L2": [1,14],
    "L4-R1": [1,14],
    "L4-R2": [1,16]
}
"""
