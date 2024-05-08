"""MAIN APP"""

from math import pi, sqrt, ceil
from handcalcs.decorator import handcalc
import handcalcs
import streamlit as st
import forallpeople as si

## Environment Setup
si.environment("default")
handcalcs.set_option("param_columns", 2)
handcalcs.set_option("line_break", "\\\[2.5pt]")
handcalcs.set_option("math_environment_start", "aligned")

MPa = 1e6 * si.Pa
mm = 1 / 1e3 * si.m

# Main title
st.title("Ingeniumarcus Research")

# Display the data
st.subheader("Simple Web App for Structural Engineering Research")

MD_INFO = """
Aplikasi web ini dikembangkan oleh tim **Ingeniumarcus**.
"""

st.markdown(MD_INFO)

st.markdown("# Parameter")

st.markdown(
    "Bagian ini mendefinisikan berbagai parameter yang digunakan dalam perhitungan"
    ", seperti kuat material, gaya, dimensi plat, dan parameter las."
)

st.markdown("## Material")


col1, col2, col3 = st.columns(3)

with col1:
    f_y = st.number_input("Kuat leleh plat $f_y (MPa)$", value=240, format="%d")
    f_y = f_y * MPa

with col2:
    f_u = st.number_input("Kuat tarik plat $f_u (MPa)$", value=440)
    f_u = f_u * MPa

with col3:
    f_u_las = st.number_input("Kuat tarik las $f_{u,las} (MPa)$", value=490)
    f_u_las = f_u_las * MPa


MD_MATERIAL = f"""
- Kuat leleh plat $f_y = {f_y:.0f}$
- Kuat tarik plat $f_u = {f_u:.0f}$
- Kuat tarik las $f_{{u,las}} = {f_u_las:.0f}$
"""

st.markdown(MD_MATERIAL)

st.markdown("## Gaya")

col1, col2 = st.columns(2)

with col1:
    diameter = st.number_input("Diameter pondasi $d (mm)$", value=1800)
    diameter = diameter * mm

with col2:
    t_casing = st.number_input("Tebal plat casing $t_{casing} (mm)$", value=14)
    t_casing = t_casing * mm

# fmt: off
@handcalc(override="params 2")
def calc_casing_area(diameter, t_casing):
    """Luas penampang casing"""
    A_n_casing = 0.25 * pi * ((diameter + (2 * t_casing)) ** 2) - (0.25 * pi * diameter**2)
    return A_n_casing
# fmt: on

ltx_casing, val_casing_area = calc_casing_area(diameter, t_casing)


@handcalc(override="long")
def calc_ultimate_force(A_n_casing, f_y):
    """Gaya ultimate"""
    P_u = A_n_casing * f_y
    return P_u


ltx_ultimate, val_ultimate_force = calc_ultimate_force(val_casing_area, f_y)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_casing)
    st.latex(ltx_ultimate)


st.markdown(
    f"""
- Diameter Pondasi $d = {diameter}$
- Tebal plat casing $t_{{casing}} = {t_casing:.0f}$
- Luas penampang casing $A_{{n,casing}} = {val_casing_area:,.0f}$
- Gaya ultimate $P_u = {val_ultimate_force:}$
"""
)


st.markdown("## Dimensi Plat")

col1, col2, col3, col4 = st.columns(4)

with col1:
    s = st.number_input("Jarak bersih antar plat penyambung $s (mm)$", value=600)
    s = s * mm

with col2:
    b_plat = st.number_input("Lebar plat $b_{plat} (mm)$", value=500)
    b_plat = b_plat * mm

with col3:
    N_p = st.number_input("Jumlah plat $N_p$", value=6)

with col4:
    L_plat = st.number_input(
        "Panjang plat yang di las pada permukaan casing $L_{plat} (mm)$", value=500
    )
    L_plat = L_plat * mm


@handcalc(override="long")
def calc_perimeter_casing(diameter, t_casing):
    """Keliling casing"""
    P_casing = pi * (diameter + 2 * t_casing)
    return P_casing


ltx_perimeter_casing, perimeter_casing = calc_perimeter_casing(diameter, t_casing)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_perimeter_casing)

## faktor reduksi penampang leleh
Phi_y = 0.9
## faktor reduksi penampang rupture
Phi_r = 0.75

st.markdown(
    f"""
    - Perimeter luar casing $P_{{casing}} = {perimeter_casing}$
    - Jarak bersih antar plat penyambung $s = {s:.0f}$
    - Lebar plat $b_{{plat}} = {b_plat:.0f}$
    - Jumlah plat $N_p = {N_p}$
    - Panjang plat yang di las pada permukaan casing $L_{{plat}} = {L_plat:.0f}$
    - Faktor reduksi penampang leleh $\Phi_y = {Phi_y}$
    - Faktor reduksi penampang _rupture_ $\Phi_r = {Phi_r}$
    """
)


st.markdown("## Parameter Las")

# ## Tebal Las
# a = 14*mm

a = st.number_input("Tebal las $a (mm)$", value=14)
a = a * mm

st.markdown(
    f"""
    - Tebal Las $a = {a:.0f}$
    """
)

st.markdown("# Analisis")

# render long
# P_u_plat = P_u/N_p
# t_plat = P_u_plat/(Phi_y*b_plat*f_y)


@handcalc(override="long")
def calc_t_plat(P_u, N_p, Phi_y, b_plat, f_y):
    """Tebal plat"""
    P_u_plat = P_u / N_p
    t_plat = P_u_plat / (Phi_y * b_plat * f_y)
    return (P_u_plat, t_plat)


ltx_t_plat, (val_P_u_plat, val_t_plat) = calc_t_plat(
    val_ultimate_force, N_p, Phi_y, b_plat, f_y
)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_t_plat)

st.markdown(
    f"""
    - Gaya ultimate plat $P_{{u,plat}} = {val_P_u_plat}$
    - Tebal plat $t_{{plat}} = {val_t_plat:.0f}$
    """
)

st.markdown("## Cek Kapasitas Tarik dan Geser Rupture")
st.markdown("### Luas efektif bidang tarik $A_et$")


@handcalc(override="long")
def calc_A_et(b_plat, t_casing):
    """Luas efektif bidang tarik"""
    A_et = b_plat * t_casing
    return A_et


ltx_A_et, val_A_et = calc_A_et(b_plat, t_casing)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_A_et)

st.markdown(f"Luas efektif bidang tarik $A_{{et}} = {val_A_et:.0f}$")

st.markdown("### Luas efektif bidang geser $A_ev$")

# %%render long
# A_ev = (L_plat*t_casing)*2


@handcalc(override="long")
def calc_A_ev(L_plat, t_casing):
    """Luas efektif bidang geser"""
    A_ev = (L_plat * t_casing) * 2
    return A_ev


ltx_A_ev, val_A_ev = calc_A_ev(L_plat, t_casing)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_A_ev)

st.markdown(f"Luas efektif bidang geser $A_{{ev}} = {val_A_ev:.0f}$")

st.markdown("### Kapasitas Rupture Pipa Casing")

# if A_et*f_u > 0.6*A_ev*f_u : P_n_rupture = 0.6*A_ev*f_y+A_et*f_u
# elif A_ev*f_u > 0.6*A_et*f_u : P_n_rupture = 0.6*A_ev*f_u+A_et*f_y
# P_n_rupture = P_n_rupture.prefix("k")
# P_r_rupture = Phi_r*P_n_rupture


@handcalc(override="long")
def calc_P_n_rupture(A_et, f_u, A_ev, f_y):
    """Kapasitas rupture"""
    if A_et * f_u > 0.6 * A_ev * f_u:
        P_n_rupture = 0.6 * A_ev * f_y + A_et * f_u
    elif A_ev * f_u > 0.6 * A_et * f_u:
        P_n_rupture = 0.6 * A_ev * f_u + A_et * f_y
    P_n_rupture = P_n_rupture.prefix("k")
    P_r_rupture = Phi_r * P_n_rupture
    return P_n_rupture, P_r_rupture


ltx_P, (p_n, p_r) = calc_P_n_rupture(val_A_et, f_u, val_A_ev, f_y)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_P)

# %%render long 2
# if P_r_rupture  > P_u_plat : Cek = "OK"
# elif P_r_rupture  < P_u_plat : Cek = "NOT OK"


@handcalc(override="long")
def check_rupture():
    if p_r > val_P_u_plat:
        Cek = "OK"
    elif p_r < val_P_u_plat:
        Cek = "NOT OK"


ltx_check_rupture, _ = check_rupture()

st.latex(ltx_check_rupture)

st.markdown("## Analisis kebutuhan Las")
st.markdown("### Tebal efektif las $t_e$")

t_e = 0.707 * a

st.markdown(f"Tebal efektif las $t_e = 0.707 \\times {a} = {t_e}$")

st.markdown("### Kuat las per mm panjang")


@handcalc(override="long")
def calc_R_r_las(Phi_r, t_e, f_u_las):
    """Kuat las per mm panjang"""
    R_r_las = Phi_r * t_e * (0.6 * f_u_las)
    R_r_las = R_r_las.prefix("k")
    return R_r_las


ltx_R_r_las, R_r_las = calc_R_r_las(Phi_r, t_e, f_u_las)

with st.expander("Detail Perhitungan"):
    st.latex(ltx_R_r_las)

st.markdown(f"Kuat las per mm panjang $R_r = {R_r_las}$")

st.markdown("### Panjang kebutuhan Las")

L_las = val_P_u_plat / R_r_las

st.markdown(
    "Panjang kebutuhan las $L_{las} = \\frac{P_{u,plat}}{R_r} = \\frac{"
    + f"{val_P_u_plat}"
    + "}{"
    + f"{R_r_las}"
    + "} = "
    + f"{L_las}$"
)
