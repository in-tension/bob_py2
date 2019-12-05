._rearranged_data = {
    <sheet_name>="cell"||"nuc" : {
        <msr_source>=(<roi_set>="cell"||"nuc"||"vor", <data_src>=("geo")||("intens", prj_method, channel)) : {
            <data_param>examp=("IntDen", "Norm") : [float]
            }
        }
    }


._rearrange_data = {
    "sheet_name" : {
        ("roi_set", ("data_type")) : {
            ("msr_param") : [float],
            ("msr_param", "calc") : [float],
            (("msr_param1", "msr_param2"), "calc") : [float]
            },

        ("roi_set", ("data_type","prj_method","ch")) : {
            ("msr_param") : [float],
            ("msr_param", "calc") : [float],
            (("msr_param1","msr_param2"), "calc") : [float]
        }
    }
}
