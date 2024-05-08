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

st.markdown(
    f"""
- Diameter Pondasi $d = {diameter}$
- Tebal plat casing $t_{{casing}} = {t_casing:.0f}$
"""
)


# fmt: off
@handcalc()
def calc_casing_area(diameter, t_casing):
    """Luas penampang casing"""
    A_n_casing = 0.25 * pi * ((diameter + (2 * t_casing)) ** 2) - (0.25 * pi * diameter**2)
    return A_n_casing
# fmt: on

ltx_casing, val_casing_area = calc_casing_area(diameter, t_casing)

st.latex(ltx_casing)


@handcalc()
def calc_ultimate_force(casing_area, f_y):
    """Gaya ultimate"""
    P_u = casing_area * f_y
    return P_u


ltx_ultimate, val_ultimate_force = calc_ultimate_force(val_casing_area, f_y)

st.latex(ltx_ultimate)
