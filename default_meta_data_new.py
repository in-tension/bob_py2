
def make_meta_data_str(exper) :

    # { <intro>
    intro = """##  any line starting with a # is a comment and is not processed by the code
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
    """
    # } </intro>

    # { <tmi>
    tmi_outer_txt = """
    ## To Measure: Intensity Parameters
    ## for each intens_im, roi_sets to measure the intensity parameters of
    ## "IntensImName" : ["RoiSetName", "RoiSetName"]
    ##
    to_msr_intens = \{
        {}
    \}
    """

    tmi_inner_txt = '    "{}" : ["Nuc"],\n'

    tmi_inner_str = ''
    for intens_im in self.hseg_intens_im_files_cab().archetype :
        tmi_inner_str += tmi_inner_txt.format(intens_im)

    tmi_str = tmi_outer_txt.format(tmi_inner_str)
    # } </tmi>

    # { <ts>
    ts_outer_txt = """## To Summarize
    ## columns to calculate summary stats for - average, total, or norm
    ## ["RoiSet", <"IntensIm">, "MsrParam"]
    to_summarize = [
        ["Vor", "Area"],
        ["Nuc", "Area"],

        {}
    ]"""

    ts_inner_txt = '''    ["{Nuc}", "{}", "Mean"],
        ["Nuc", "{}", "IntDen"]\n\n,'''

    ts_inner_str = ''
    for intens_im in self.hseg_intens_im_files_cab().archetype :
        ts_inner_str += ts_inner_txt.format(intens_im, intens_im)

    ts_str = ts_outer_txt.format(ts_inner_str)
    # } </ts>

    # { <iitc>
    iitc_str = """
    ## ---------- optional variables ----------
    ##
    ## Intensity Images to Create
    ##      intens_im that bob_py should autogenerate
    ##      a z-projection of a channel
    ## optional, but if used, requires hseg_slices
    ## "IntensImName" : (num, "prjmethod")
    intens_im_to_create = {
        # "Hoe" : (4, "sum"),
    }"""
    # } </iitc>

    # { <hss>
    hss_outer_txt = """
    ## Hemisegment Slices
    ##      the start and end z-slices for each hemisegment
    ## "Hemisegment-Name" : [start, end]
    hseg_slices = /{
        {}
    /}
    """

    hss_inner_txt = '    "{}": [1, ],\n'

    hss_inner_str = ''
    for hseg in self.hsegs() :
        hss_inner_str += hss_inner_txt.format(hseg.name)

    hss_str = hss_out_txt.format(hss_inner_str)
    # } </hss>


    meta_data_str = intro + tmi_str + ts_str + iitc_str + hss_str
    return meta_data_str
