"""
Date-based FAO-56 crop coefficient curve construction.
Matches SWB2 Fortran implementation in crop_coefficients__fao56.F90,
function update_crop_coefficient_date_as_threshold().
"""
import datetime as dt
import numpy as np


def compute_growth_stage_dates(planting_date, l_ini, l_dev, l_mid, l_late, l_fallow):
    """Compute the endpoint dates for each growth stage.

    Args:
        planting_date: datetime.date for planting
        l_ini, l_dev, l_mid, l_late, l_fallow: length in days of each stage

    Returns:
        dict with keys: planting, end_ini, end_dev, end_mid, end_late, end_fallow
    """
    end_ini = planting_date + dt.timedelta(days=l_ini)
    end_dev = end_ini + dt.timedelta(days=l_dev)
    end_mid = end_dev + dt.timedelta(days=l_mid)
    end_late = end_mid + dt.timedelta(days=l_late)
    end_fallow = end_late + dt.timedelta(days=l_fallow)

    return dict(planting=planting_date, end_ini=end_ini, end_dev=end_dev,
                end_mid=end_mid, end_late=end_late, end_fallow=end_fallow)


def update_crop_coefficient_date(current_date, stages, kcb_ini, kcb_mid, kcb_end, kcb_min):
    """Compute Kcb for a given date based on growth stage dates.

    Matches the Fortran logic exactly:
      - After date_late: kcb_min
      - date_mid to date_late: linear interp from kcb_mid to kcb_end
      - date_dev to date_mid: kcb_mid (plateau)
      - date_ini to date_dev: linear interp from kcb_ini to kcb_mid
      - planting to date_ini: kcb_ini
      - Before planting: kcb_min

    Args:
        current_date: datetime.date
        stages: dict from compute_growth_stage_dates()
        kcb_ini, kcb_mid, kcb_end, kcb_min: crop coefficient values

    Returns:
        float: Kcb value for the current date
    """
    if current_date >= stages['end_late']:
        return kcb_min
    elif current_date >= stages['end_mid']:
        days_since = (current_date - stages['end_mid']).days
        days_total = (stages['end_late'] - stages['end_mid']).days
        frac = days_since / days_total if days_total > 0 else 0.0
        return kcb_mid * (1.0 - frac) + kcb_end * frac
    elif current_date >= stages['end_dev']:
        return kcb_mid
    elif current_date >= stages['end_ini']:
        days_since = (current_date - stages['end_ini']).days
        days_total = (stages['end_dev'] - stages['end_ini']).days
        frac = days_since / days_total if days_total > 0 else 0.0
        return kcb_ini * (1.0 - frac) + kcb_mid * frac
    elif current_date >= stages['planting']:
        return kcb_ini
    else:
        return kcb_min


def compute_kcb_timeseries(start_date, end_date, planting_doy,
                           l_ini, l_dev, l_mid, l_late, l_fallow,
                           kcb_ini, kcb_mid, kcb_end, kcb_min):
    """Compute a full Kcb timeseries, handling multi-year date resets.

    At the end of the fallow period, the planting date advances to the
    next occurrence (same DOY, next year if already past).

    Args:
        start_date, end_date: datetime.date
        planting_doy: day of year for planting
        l_ini, l_dev, l_mid, l_late, l_fallow: stage lengths in days
        kcb_ini, kcb_mid, kcb_end, kcb_min: Kcb values

    Returns:
        dates: list of datetime.date
        kcb_values: list of float
    """
    # Initialize planting date for the start year
    planting_date = dt.date(start_date.year, 1, 1) + dt.timedelta(days=planting_doy - 1)
    if planting_date < start_date:
        # If we're already past planting in the start year, still use it
        # (SWB2 initializes with the start year's planting date)
        pass

    stages = compute_growth_stage_dates(planting_date, l_ini, l_dev, l_mid, l_late, l_fallow)

    dates = []
    kcb_values = []
    current = start_date

    while current <= end_date:
        # Check if we need to advance to next year's planting cycle
        if current > stages['end_fallow']:
            # Advance planting date to next occurrence
            next_planting = dt.date(current.year, 1, 1) + dt.timedelta(days=planting_doy - 1)
            if current.timetuple().tm_yday > planting_doy:
                next_planting = dt.date(current.year + 1, 1, 1) + dt.timedelta(days=planting_doy - 1)
            stages = compute_growth_stage_dates(next_planting, l_ini, l_dev, l_mid, l_late, l_fallow)

        kcb = update_crop_coefficient_date(current, stages, kcb_ini, kcb_mid, kcb_end, kcb_min)
        dates.append(current)
        kcb_values.append(kcb)
        current += dt.timedelta(days=1)

    return dates, kcb_values
