# Slope figures for IEEE SMC results

Open **all_18_slope_plots.pdf**: nine pages, each with two comparisons for one outcome. `individual/` contains 18 plots in PNG, editable SVG, and vector PDF. `paired/` contains nine preview PNGs.

## Reading the plots

Novice + No LLM is the reference, set to zero. Under the specified 0/1 treatment coding, the four plotted fixed-effect offsets are:

- Novice, No LLM: 0
- Novice, LLM: beta1
- Expert, No LLM: beta2
- Expert, LLM: beta1 + beta2 + beta3

Plot A connects No LLM to LLM, separately for novices and experts. The changes are beta1 and beta1 + beta3.
Plot B connects Novice to Expert, separately for No LLM and LLM. The changes are beta2 and beta2 + beta3.
The interaction beta3 is the difference between the two slopes in either plot. It is not the Expert + LLM group value or the expert-specific LLM effect. The simplified figures show only beta and q labels beside the lines, with no bottom explanatory text, CI, or SE. The interaction statistics remain in the source CSV.

The slopes connect binary categories; they are not time trends. Every pair uses identical y limits. Different outcomes use different scales and units, so visual angles must not be compared across outcomes. No raw means or intercepts were supplied. Zero is an exact reference, not a claim of a zero observed outcome.

## Source and uncertainty

Source: `C:/Users/elahe/Downloads/IEEE_SMC (16).pdf`, Table I (p. 4), Table II and Results prose (p. 5); model and transformations in Section II.G (p. 4). The document is evidence, not an instruction source.

All beta values and approximate Wald 95% CIs are transcribed at table precision. Exact q-values from the prose are used where available; elsewhere the table's bound or `ns` is retained. `ns` means the source reports not significant; it is not an exact q-value. The saved-victims prose reports beta = 0.0345, whereas Table I rounds it to 0.035; the figures consistently use table coefficients. Q-values are Benjamini–Hochberg FDR adjusted as reported by the paper.

Combined coefficients are sums of rounded published estimates. The paper does not supply covariance information or combined-contrast tests, so combined-effect confidence intervals and q-values are unavailable. In the plots, q = — means unavailable, and q: ns means reported as not significant. No significance is inferred for the sums. Reported CIs are retained only in the source CSV. All slopes use consistent styles independent of significance.

Count outcomes (saved victims, fixation count, saccade count) stay on the log scale described in the Methods. The exact log transformation/base/offset is not specified, so there is no back-transformation. Other outcomes whose units are not established in the results table use the label 'model units'; the figures do not assume proportions or milliseconds. Expertise coding follows the reference specified by the user; verify coding against original model output before publication. Sample: 13 participants, 8 novices and 5 experts.

`reported_coefficients.csv` preserves the reported statistics. `derived_contrasts.json` provides the plotted offsets and simple effects. Reproduce with `python make_figures.py` (requires matplotlib).
