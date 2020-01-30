
raw_stack_mode =

hseg_slices = {
    "HsegName": [startSlice, endSlice],
    "": [],
    "": [],
}

## you need this to have any output
to_process = [
##  ["roi_set"]                 where roi_sets = ["Cell", "Vor", "Nuc"]
##  ["roi_set", <channel>]
##  where <channel> can be
##   n                  where n is an integer  (prj_method defaults to "sum")
##   [n, "prj_method"]
##   "channel_name"     if there is a channel_dict
    ["Cell"],
    ["Vor"],
    ["Nuc"],
    ["Nuc", 1],
    ["Nuc", [2, "sum"]],
    ["Nuc", 3],
    ["Nuc", "Hoe"]
]

## optional - if you refer to channels by a name in other fields or you want the name to be used in output, you need this
channel_dict = {
    "H3K9ac": [1, "sum"],   ## [channel_num, zprojection_method]
    "Fib-bin": 2,   ## sum can be omitted because it's the default
    "Phal": 3,      ## if prj_method is included, you must have []
    "Hoe": 4}

## optional - you need this to get "Norm", "Tot", or "Avg" columns
to_summarize = [
    ["Vor", "Area"],
    ["Nuc", "Area"],
    ## ["Nuc", "NND"],
    ## ["Nuc", "Hoe", "Ploidy"],
    ["Nuc", "Hoe", "Mean"],
    ["Nuc", "Hoe", "IntDen"],
    ["Nuc", "H3K9ac", "IntDen"],

    ["Nuc", "Fib-bin", "Mean"],
    ["Nuc", "Fib-bin", "IntDen"]]


projection_mode = """


"""
