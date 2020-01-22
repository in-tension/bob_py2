
ihe_dict = {
"cell_sheet" : {
    ("Cell","Geo") : [
        "Area",
        "Perim",
        "BX",
        "BY",
        "Width",
        "Height",
        "AR"],

    ("Vor", "Geo") : [
        ("Area", "Avg"),
        ("Area", "Sum")],
    ("Nuc", "Geo") : [
        ("Area", "Avg"),
        ("Area", "Sum"),
        ("NND", "Avg")],
    ("Nuc", ("Intens", "sum", "Hoechst")) : [
        ("Ploidy", "Avg"),
        ("Ploidy", "Sum"),
        ("IntDen", "Avg"),
        ("IntDen", "Sum")],
    ("Nuc", ("Intens", "sum", "Fibrillarin")) : [
        ("Mean", "Avg"),
        ("Mean", "Sum"),
        ("IntDen", "Avg"),
        ("IntDen", "Sum")]},

"nuc_sheet" : {
    ("Nuc", "Geo") : [
        "Area",
        ("Area", "Norm"),
        "X",
        (("Y", ("Cell", "Geo", "Height")), "Rel Y"),
        "Perim"
        "AR",
        "NND",
        ("NND", "Norm")],
    ("Nuc", ("Intens", "sum", "Hoechst")) : [
        "Mean",
        ("Mean", "Norm"),
        "StdDev",
        "IntDen",
        ("IntDen", "Norm"),
        "RawIntDen",
        ("Special", "Ploidy"),
        ("Ploidy", "Norm")],
    ("Nuc", ("Intens", "sum", "Fibrillarin")) : [
        "Mean",
        ("Mean", "Norm"),
        "StdDev",
        "IntDen",
        "RawIntDen",
        "AreaFrac",
        "Area"],
    ("Nuc", ("Intens", "sum", "H3K9ac")) : [
        "Mean",
        "StdDev",
        "IntDen",
        ("IntDen", "Norm"),
        "RawIntDen"],
    ("Vor", "Geo") : [
        "Area",
        ("Area", "Norm"),
        "Perim",
        "AreaFrac"]}    ## areafrac of binary in vor roi

}
