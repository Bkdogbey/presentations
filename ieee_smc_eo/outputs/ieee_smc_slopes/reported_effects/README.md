# Reported coefficients

These nine figures supersede the earlier combined-effect plots. Each shows the three coefficients directly from Tables I–II of IEEE_SMC (16).pdf (pp. 4–5). Beta values and q bounds / ns match the tables exactly; more precise prose q-values are not substituted. No coefficient sums are plotted.

Each slope connects zero effect to a reported coefficient. The endpoints are a visual encoding of a coefficient, not group means or a time trend. With Novice + No LLM as the model reference, LLM is the LLM effect among novices; Expertise is expert versus novice without LLM; LLM × Expertise is the difference in those conditional effects (the interaction). The interaction is not an Expert + LLM group estimate.

The three panels use the same vertical scale within an outcome; scales differ across outcomes. Count outcomes remain on the modeled log scale. ns means reported as not significant, not a numeric q-value. No CI, SE, or explanatory footer appears in the figures.

Source data and rendering scripts are included in the ZIP. Run `python make_reported_effects.py` in this directory (matplotlib required).
