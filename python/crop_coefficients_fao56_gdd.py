import numpy as np

def update_crop_coefficient_by_gdd(gdd_plant: float,
                                     gdd_ini: float,
                                     gdd_dev: float,
                                     gdd_mid: float,
                                    gdd_late: float,
                                  gdd_fallow: float,
                                     kcb_min: float,
                                     kcb_ini: float,
                                     kcb_mid: float,
                                     kcb_end: float,
                                         gdd: float):
    """Update crop coefficient given the current gdd.

    Args:
        gdd_plant (float): _description_
        gdd_ini (float): _description_
        gdd__dev (float): _description_
        gdd_mid float): _description_
        gdd_late (float): 
        kcb_min (float): _description_
        kcb_mid (float): _description_
        kcb_kcb_end (float): _description_
        gdd (float): _description_

                                    kcb_mid
                            /----------------------\
                           /                        \
                          /                          \
                         /                            \
                        /                              \
                       /                                \
                      /                                  \
        kcb_ini      /                                    \      kcb_end
    ----------------/                                      \----------------
    |               |       |                      |       |                |
 gdd_plant       gdd_ini  gdd_mid              gdd_late  gdd_fallow
    
    """

    # ! now calculate Kcb for the given landuse
    # if( fGDD > GDD_late_l ) then
    #   fKcb = Kcb_min
    # elseif ( fGDD > GDD_mid_l ) then
    #   fFrac = ( fGDD - GDD_mid_l ) / ( GDD_late_l - GDD_mid_l )
    #   fKcb =  Kcb_mid * (1.0_c_double - fFrac) + Kcb_end * fFrac
    # elseif ( fGDD > GDD_dev_l ) then
    #   fKcb = Kcb_mid
    # elseif ( fGDD > GDD_ini_l ) then
    #   fFrac = ( fGDD - GDD_ini_l ) / ( GDD_dev_l - GDD_ini_l )
    #   fKcb = Kcb_ini * (1_c_double - fFrac) + Kcb_mid * fFrac
    # elseif ( (PlantingDOY > 0) .and. (current_DOY >= PlantingDOY) ) then
    #   ! if there is a valid value for the Planting Date, use it
    #   fKcb = Kcb_ini
    # elseif ( (GDD_plant_l >= 0.) .and. (fGDD >= GDD_plant_l) ) then
    #     fKcb = Kcb_ini
    # else
    #   fKcb = Kcb_min
    # endif


    if gdd > gdd_fallow:
        # TODO: possibly interpolate between kcb_end and kcb_min during l_fallow period
        kcb = kcb_min
    elif gdd > gdd_late:
        kcb = kcb_end
    elif gdd > gdd_mid:
        frac = ( gdd - gdd_mid ) / ( gdd_late - gdd_mid )
        kcb = kcb_mid * (1.0 - frac) + kcb_end * frac
    elif gdd > gdd_dev:
       kcb = kcb_mid
    elif gdd > gdd_ini:
        frac = ( gdd - gdd_plant ) / ( gdd_dev - gdd_plant )
        kcb = kcb_ini * (1.0 - frac) + kcb_mid * frac
    else:
       kcb = kcb_min

    return kcb
