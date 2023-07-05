# Accelerometer_Plot

Codes to plot raw accelerometer data obtained by TADAS Stations [AFAD](https://tadas.afad.gov.tr/map).

* Velocity values are derived by using acceleration values with followed formula,
$\frac{a_{t+1} - a_{t}}{\Delta t}$

* Displacement values are derived by using velocity values with followed formula,
$\frac{v_{t+1} - v_{t}}{\Delta t}$

The functions required for the inverse problem (displacement -> velocity -> acceleration) are also available in the file, if needed.

Example input:

Raw accelerometer data of 06.02.2023 01:17:34 (UTC) Pazarcık (Kahramanmaraş) MW 7.4 Earthquake (AFAD - TADAS) records are located in [data](https://github.com/Bilalhappy/Accelerometer_Plot/tree/main/data) directory.

Example output:

<div align="center">
    <img src="https://github.com/Bilalhappy/Accelerometer_Plot/blob/main/Pazarcık_ENH.png">
</div>



