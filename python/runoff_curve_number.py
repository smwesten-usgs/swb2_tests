import numpy as np


def calculate_cn_S_inches(curve_number):
    """
    Return the curve number storage (S) term, in inches. Equation 2-4, Cronshey and others (1986).
    """
    S_inches = (1000.0 / curve_number) - 10.0
    return S_inches


def calculate_cn_S_millimeters(curve_number):
    """
    Return the curve number storage (S) term, in millimeters. Equation 2-4, Cronshey and others (1986),
    with constants multiplied by 25.4 (mm to inches).
    """
    S_mm = (25400.0 / curve_number) - 254.0
    return S_mm


def calculate_cn_runoff_inches(inflow_inches, curve_num_adj):
    """
    Calculate runoff in inches given inflow and adjusted curve number.
    Matches SWB2 Fortran implementation in runoff__curve_number.F90:
      1. Smax = (1000 / CN_adj) - 10
      2. Smax = 1.33 * Smax^1.15   (Woodward and others, 2003, eq. 8)
      3. If inflow > 0.05*Smax: runoff = (inflow - 0.05*Smax)^2 / (inflow + 0.95*Smax)
    """
    Smax = (1000.0 / curve_num_adj) - 10.0
    Smax = 1.33 * (Smax ** 1.15)

    runoff = np.where(inflow_inches > 0.05 * Smax,
                      (inflow_inches - 0.05 * Smax) ** 2 / (inflow_inches + 0.95 * Smax),
                      0.0)
    return runoff


def calculate_cn_alternative_S_0_05(storage_S):
    """
    Return the adjusted curve number storage term for Ia = 0.05*S (rather than 0.2*S).
    Equation 8, Woodward and others (2003).
    """
    return 1.33 * (storage_S ** 1.15)


def calculate_cn_arc2_to_arc1(curve_number_arc2):
    """
    Return a curve number corresponding to antecedent runoff condition 1, given a
    curve number corresponding to antecedent runoff condition 2.
    Equation 3.145, Mishra and Singh (2003); equation 15, Ponce and Hawkins (1996).
    Resulting curve numbers are clipped to the range 30-100.
    """
    return np.clip(curve_number_arc2 / (2.281 - 0.01281 * curve_number_arc2),
                   30.0, 100.0)


def calculate_cn_arc2_to_arc3(curve_number_arc2):
    """
    Return a curve number corresponding to antecedent runoff condition 3, given a
    curve number corresponding to antecedent runoff condition 2.
    Equation 3.146, Mishra and Singh (2003); equation 16, Ponce and Hawkins (1996).
    Resulting curve numbers are clipped to the range 30-100.
    """
    return np.clip(curve_number_arc2 / (0.427 + 0.00573 * curve_number_arc2),
                   30.0, 100.0)


def calculate_probability_of_enhanced_runoff(cfgi, cfgi_ll, cfgi_ul):
    """
    Return the probability of enhanced runoff due to frozen ground conditions.
    Matches SWB2 Fortran function prob_runoff_enhancement().

    Linear interpolation between 0 (at cfgi_ll) and 1 (at cfgi_ul).
    """
    if cfgi <= cfgi_ll:
        return 0.0
    elif cfgi >= cfgi_ul:
        return 1.0
    else:
        return (cfgi - cfgi_ll) / (cfgi_ul - cfgi_ll)


def adjust_curve_number(curve_number_arc2, inflow_5_day_sum, is_growing_season=False,
                        cfgi=0.0, cfgi_ll=55.0, cfgi_ul=83.0):
    """
    Adjust the curve number based on antecedent moisture conditions and frozen ground.
    Matches SWB2 Fortran function update_curve_number_fn().

    The Fortran implementation uses:
      - CFGI > cfgi_ll AND soil_storage_max > 0: use probability-weighted CN_II/CN_III
      - Growing season: 5-day rainfall thresholds of 1.40 (dry) and 2.10 (wet) inches
      - Dormant season: 5-day rainfall thresholds of 0.50 (dry) and 1.10 (wet) inches

    Returns the adjusted curve number (scalar).
    """
    AMC_DRY_GROWING = 1.40
    AMC_DRY_DORMANT = 0.50
    AMC_WET_GROWING = 2.10
    AMC_WET_DORMANT = 1.10

    cn_arc1 = calculate_cn_arc2_to_arc1(curve_number_arc2)
    cn_arc3 = calculate_cn_arc2_to_arc3(curve_number_arc2)

    if cfgi > cfgi_ll:
        p_er = calculate_probability_of_enhanced_runoff(cfgi, cfgi_ll, cfgi_ul)
        cn_adj = curve_number_arc2 * (1.0 - p_er) + cn_arc3 * p_er

    elif is_growing_season:
        if inflow_5_day_sum < AMC_DRY_GROWING:
            cn_adj = cn_arc1
        elif inflow_5_day_sum >= AMC_WET_GROWING:
            cn_adj = cn_arc3
        else:
            cn_adj = curve_number_arc2

    else:  # dormant season
        if inflow_5_day_sum < AMC_DRY_DORMANT:
            cn_adj = cn_arc1
        elif inflow_5_day_sum >= AMC_WET_DORMANT:
            cn_adj = cn_arc3
        else:
            cn_adj = curve_number_arc2

    return np.clip(cn_adj, 30.0, 100.0)


def cn_references():
    """
    Cronshey, R., McCuen, R., Miller, N., Rawls, W., Robbins, S., and Woodward, D., 1986, Urban Hydrology
        for Small Watersheds - Technical release 55: US Dept. of Agriculture, Soil Conservation Service,
        Engineering Division, accessed at http://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/16/stelprdb1044171.pdf.

    Mishra, S.K., and Singh, V.P., 2003, Soil Conservation Service Curve Number (SCS-CN) Methodology: Water Science
         and Technology Library, Springer Netherlands, Dordrecht, 534 p.

    Ponce, V.M., and Hawkins, R.H., 1996, Runoff Curve Number: Has It Reached Maturity? Journal of Hydrologic
        Engineering, v. 1, no. 1, p. 11-19.

    Woodward, D.E., Hawkins, R.H., Jiang, R., Hjelmfelt, J., Van Mullem, J.A., and Quan, Q.D., 2003,
        Runoff Curve Number Method: Examination of the Initial Abstraction Ratio,
        in World Water and Environmental Resources Congress 2003,
        American Society of Civil Engineers, Philadelphia, Pennsylvania, p. 1-10.

    """
    pass
