# grain-growth
## Grain Growth Calculator

Codes were written for the calculation of "Coarsening of polyhedral grains in a liquid matrix."


Reference: Journal of Materials Research, Vol. 24, 2949-2959 (2009)

The coarsening of polyhedral grains in a liquid matrix was calculated using crystal growth and dissolution equations used in crystal growth theories for faceted crystals. The coarsening behavior was principally governed by the relative value of the maximum driving force for growth (Δgmax), which is determined by the average size and size distribution, to the critical driving force for appreciable growth (Δgc). When Δgmax was much larger than Δgc, pseudonormal grain coarsening occurred. With a reduction of Δgmax relative to Δgc, abnormal grain coarsening (AGC, when Δgmax ≥ Δgc) and stagnant grain coarsening (SGC, when Δgmax < Δgc) were predicted. The observed cyclic AGC and incubation for AGC in real systems with faceted grains were explained in terms of the relative value between Δgmax and Δgc. The effects of various processing and physical parameters, such as the initial grain size and distribution, the liquid volume fraction, step free energy, and temperature, were also evaluated. The calculated results were in good agreement with previous experimental observations.

## Screenshot

<img width="752" alt="Screenshot 2023-09-21 223121" src="https://github.com/e99ward/grain-growth/assets/103809702/2f1e45a4-a7d4-42ba-a596-a9e4c5890f80">

## Usage

First use: Generate initial dataset (set of grain sizes) on the third box run "generate" -> dataset file will be generated in same folder named "d_0000000.txt.npy"

Calculation: Set up the calculation parameters and datasets to be saved.
- dataset can be read by numpy package.
- filename of the dataset means the CTS (calculation time step)
- you can restart the calculation from any CTS if you have dataset at the CTS "d_0000100.txt" (100 CTS)

Visualization
- The average grain size and maximum grain size are showing every 10 CTS.
- The scrollbar next to the Progress_CTS provides the grain size histogram for the saved dataset.

<img width="752" alt="Screenshot 2023-09-21 223248" src="https://github.com/e99ward/grain-growth/assets/103809702/bcae3386-eac8-4fc3-b738-5fb9425ce7a2">
