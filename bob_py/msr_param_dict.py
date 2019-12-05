
msr_param_dict = {
"cell_sheet" : {
    ("cell","geo") : [
        "Area",
        "Perim",
        "BX",
        "BY",
        "Width",
        "Height",
        "AR"],

    ("vor", "geo") : [
        ("Area", "Avg"),
        ("Area", "Sum")],
    ("nuc", "geo") : [
        ("Area", "Avg"),
        ("Area", "Sum"),
        ("NND", "Avg")],
    ("nuc", ("intens", "sum", "Hoechst")) : [
        ("Ploidy", "Avg"),
        ("Ploidy", "Sum"),
        ("IntDen", "Avg"),
        ("IntDen", "Sum")],
    ("nuc", ("intens", "sum", "Fibrillarin")) : [
        ("Mean", "Avg"),
        ("Mean", "Sum"),
        ("IntDen", "Avg"),
        ("IntDen", "Sum")]},

"nuc_sheet" : {
    ("nuc", "geo") : [
        "Area",
        ("Area", "Norm"),
        "X",
        (("Y", ("cell", "geo", "Height")), "Rel Y"),
        "Perim"
        "AR",
        "NND",
        ("NND", "Norm")],
    ("nuc", ("intens", "sum", "Hoechst")) : [
        "Mean",
        "Norm_Mean",
        "StdDev",
        "IntDen",
        ("IntDen", "Norm"),
        "RawIntDen",
        ("Special", "Ploidy"),
        ("Ploidy", "Norm")],
    ("nuc", ("intens", "sum", "Fibrillarin")) : [
        "Mean",
        ("Mean", "Norm"),
        "StdDev",
        "IntDen",
        "RawIntDen",
        "AreaFrac",
        "Area"],
    ("nuc", ("intens", "sum", "H3K9ac")) : [
        "Mean",
        "StdDev",
        "IntDen",
        ("IntDen", "Norm"),
        "RawIntDen"],
    ("nuc", "geo") : [
        "Area",
        ("Area", "Norm"),
        "Perim",
        "AreaFrac"]}

}
