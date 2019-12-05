
._data = {
    ("roi_group", (<msrment_source>)) : {
        "msrment_parameter" : [float]
        }
    }

hseg._data = {
    ("cell", ("geo")) : {
        examp="Area" : [float]
        }
    }

cell._data = {
    ("nuc"||"vor", ("geo")) : {
        examp="Area" : [float]
        },
    ("nuc"||"vor", ("intens", "sum", "Hoechst")) : {
        examp="Mean" : [float]
        }
    }
