

cell_conv_hdings = [
    "Area",
    "Perim",
    "BX",
    "BY",
    "Width",
    "Height",
    "AR",

    "Avg_Area_Vor",         ## "Vor_Avg_Area"
    "Sum_Area_Vor",         ## "Vor_Sum_Area"


    "Avg_Area_Nuc",
    "Sum_Area_Nuc",
    "Avg_NND",

    "Avg_Ploidy",
    "Sum_Ploidy",

    "Avg_IntDen_Hoe",       ## HoeAvgIntDen or Hoe_Avg_IntDen
    "Sum_IntDen_Hoe",

    "Avg_Mean_Fib",
    "Sum_Mean_Fib",
    "Avg_IntDen_Fib",
    "Sum_IntDen_Fib"
]


nuc_conv_hdings = {
    "Geo": [
        "Area",
        "Norm_Area",
        "X",
        "Rel_Y",
        "Perim"
        "AR",
        "NND"
        "Norm_NND"
    ],
    "hoe": [
        "Mean",
        "Norm_Mean",
        "StdDev",
        "IntDen",
        "Norm_IntDen"
        "RawIntDen",
        "Ploidy",
        "Norm_Ploidy"
    ],
    "h3k9ac": [
        "Mean",
        "StdDev",
        "IntDen",
        "Norm_IntDen",
        "RawIntDen"
    ],
    "fib": [
        "Mean",
        "Norm_Mean"
        "StdDev",
        "IntDen",
        "RawIntDen",
        "AreaFrac",
        "Area"
    ],
    "Vor": [        ## in the order do you want voronoi
        "Area",
        "Norm_Area",
        "Perim",
        "AreaFrac"
    ]
}
