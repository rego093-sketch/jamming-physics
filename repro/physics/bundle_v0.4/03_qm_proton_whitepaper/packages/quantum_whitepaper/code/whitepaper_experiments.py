"""Minimal numerical experiments for the hydrodynamic proton-radius white paper.

Experiments implemented
-----------------------
1) Proton radius from hydrodynamic model:
   R_p = (2/pi) * lambda_C, where lambda_C = h / (m_p c).

2) Collapse–stiffness balance:
   p_in(x)    = x^(-4),
   p_stiff(x) = alpha * x^(-5), alpha = 2/pi.
   We tabulate both curves over a range of x = R/L_q.

3) Sensitivity of R_p to geometric factor alpha:
   R_p(alpha) = alpha * lambda_C.
   We vary alpha around 2/pi and record the linear response.

4) Length selection from the Swift–Hohenberg dispersion relation:
   k_star^2 = epsilon / (2 sigma),
   L_star   = 2*pi / k_star  ∝  (sigma/epsilon)^(1/2).
   We sample (epsilon, sigma) pairs and check that
   L_star / sqrt(sigma/epsilon) is approximately constant.

Running this file will (re)generate all CSV data in the ./data directory.
"""

import os
from math import pi

import numpy as np
import pandas as pd


# --- Experiment 1: proton radius from hydrodynamic model -----------------


def experiment1_proton_radius() -> pd.DataFrame:
    """Compute lambda_C and R_p = (2/pi) * lambda_C in femtometres.

    We also record a representative experimental value and the relative
    difference, as quoted in the continuum toy model manuscript.
    """
    # Physical constants (SI)
    h = 6.62607015e-34       # Planck constant [J s]
    c = 2.99792458e8         # speed of light [m/s]
    m_p = 1.6726219e-27      # proton mass [kg]

    lambda_C_m = h / (m_p * c)
    lambda_C_fm = lambda_C_m * 1e15

    alpha_geom = 2.0 / pi
    Rp_theory_fm = alpha_geom * lambda_C_fm

    # Representative experimental value (not used to tune the model)
    Rp_exp_fm = 0.8414
    Rp_exp_err_fm = 0.0019

    delta_R = Rp_theory_fm - Rp_exp_fm
    rel_diff = delta_R / Rp_exp_fm

    df = pd.DataFrame(
        [
            {
                "h_SI": h,
                "c_SI": c,
                "m_p_SI": m_p,
                "lambda_C_fm": lambda_C_fm,
                "alpha_geom_2_over_pi": alpha_geom,
                "Rp_theory_fm": Rp_theory_fm,
                "Rp_exp_fm": Rp_exp_fm,
                "Rp_exp_err_fm": Rp_exp_err_fm,
                "delta_R_fm": delta_R,
                "relative_diff_Rp": rel_diff,
            }
        ]
    )
    return df


# --- Experiment 2: collapse–stiffness balance ----------------------------


def experiment2_pressures(alpha_geom: float,
                          n_points: int = 200,
                          x_min: float = 0.2,
                          x_max: float = 3.0) -> pd.DataFrame:
    """Tabulate p_in(x) and p_stiff(x) on a 1D grid in x = R/L_q."""
    x = np.linspace(x_min, x_max, n_points)
    p_in = x ** -4
    p_stiff = alpha_geom * x ** -5

    df = pd.DataFrame(
        {
            "x_R_over_Lq": x,
            "p_in_x_minus_4": p_in,
            "p_stiff_alpha_x_minus_5": p_stiff,
            "p_in_minus_p_stiff": p_in - p_stiff,
        }
    )
    return df


# --- Experiment 3: sensitivity to alpha ----------------------------------


def experiment3_alpha_sensitivity(lambda_C_fm: float,
                                  alpha_center: float,
                                  rel_range: float = 0.1,
                                  n_points: int = 101) -> pd.DataFrame:
    """Scan alpha around 2/pi and record the induced change in R_p.

    The analytic relation is R_p(alpha) = alpha * lambda_C.
    Therefore delta R_p / R_p0 = delta alpha / alpha_center.
    We verify this numerically on a grid.
    """
    alphas = np.linspace(
        alpha_center * (1.0 - rel_range),
        alpha_center * (1.0 + rel_range),
        n_points,
    )
    Rp = alphas * lambda_C_fm
    Rp0 = alpha_center * lambda_C_fm

    rel_change_alpha = (alphas - alpha_center) / alpha_center
    rel_change_Rp = (Rp - Rp0) / Rp0

    df = pd.DataFrame(
        {
            "alpha_geom": alphas,
            "Rp_fm": Rp,
            "relative_change_alpha": rel_change_alpha,
            "relative_change_Rp": rel_change_Rp,
        }
    )
    return df


# --- Experiment 4: Swift–Hohenberg length selection ----------------------


def experiment4_length_selection(n_grid: int = 40) -> pd.DataFrame:
    """Sample (epsilon, sigma) pairs and compute L_star.

    We use the linear dispersion
        k_star^2 = epsilon / (2 sigma),
        L_star   = 2*pi / k_star,
    then check that the rescaled length
        L_star / sqrt(S),  S = sigma/epsilon,
    is approximately constant and independent of epsilon, sigma.
    """
    epsilons = np.linspace(0.5, 2.0, n_grid)
    sigmas = np.linspace(0.5, 2.0, n_grid)

    rows = []
    for eps in epsilons:
        for sig in sigmas:
            S = sig / eps
            k_star = (eps / (2.0 * sig)) ** 0.5
            L_star = 2.0 * pi / k_star
            scaled = L_star / (S ** 0.5)
            rows.append(
                {
                    "epsilon": eps,
                    "sigma": sig,
                    "S_ratio_sigma_over_epsilon": S,
                    "k_star": k_star,
                    "L_star": L_star,
                    "scaled_length_Lstar_over_sqrt_S": scaled,
                }
            )

    df = pd.DataFrame(rows)
    return df


# --- Main entry point ----------------------------------------------------


def main(base_dir: str | None = None) -> None:
    """Run all four experiments and write CSVs under base_dir/data.

    Parameters
    ----------
    base_dir:
        Path to the quantum_whitepaper package root. If None, we assume
        that this file lives in <base_dir>/code/ and climb one level up.
    """
    if base_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(here, ".."))

    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    alpha_geom = 2.0 / np.pi

    # Experiment 1
    exp1 = experiment1_proton_radius()
    exp1.to_csv(
        os.path.join(data_dir, "experiment1_proton_radius.csv"),
        index=False,
    )

    lambda_C_fm = float(exp1["lambda_C_fm"].iloc[0])

    # Experiment 2
    exp2 = experiment2_pressures(alpha_geom=alpha_geom)
    exp2.to_csv(
        os.path.join(data_dir, "experiment2_collapse_stiffness_balance.csv"),
        index=False,
    )

    # Experiment 3
    exp3 = experiment3_alpha_sensitivity(
        lambda_C_fm=lambda_C_fm,
        alpha_center=alpha_geom,
    )
    exp3.to_csv(
        os.path.join(data_dir, "experiment3_alpha_sensitivity.csv"),
        index=False,
    )

    # Experiment 4
    exp4 = experiment4_length_selection()
    exp4.to_csv(
        os.path.join(data_dir, "experiment4_length_selection_dispersion.csv"),
        index=False,
    )

    print("Experiments completed. Data written to:", data_dir)


if __name__ == "__main__":
    import sys

    user_base_dir = sys.argv[1] if len(sys.argv) > 1 else None
    main(base_dir=user_base_dir)
