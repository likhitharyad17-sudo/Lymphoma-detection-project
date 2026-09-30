# Final Minor Corrections Changelog

**Manuscript Title:** Attention-Augmented Residual Deep Learning Framework for Lymphoma Detection  
**Review Pass:** Final Minor Publication Corrections Pass  
**Status:** Complete & Verified  

---

### Summary of the Four Applied Corrections

1. **Correction 1 — Remove "Calibrated" from Figure 7 (and Manuscript Text):**
   - In Figure 7(b) (`figures/fig8_ablation_threshold.pdf` and `figures/fig8_ablation_threshold.png`), changed the legend label from `"Calibrated \tau = 0.80"` to `"Validation-selected \tau = 0.80"`.
   - In Section IV-A (`main.tex`), changed `"calibrated on 15% validation ($N=56$)"` to `"evaluated on 15% validation ($N=56$)"`.
   - Verified that no other figure, caption, table, or paragraph incorrectly describes $\tau = 0.80$ as calibrated or as an optimal OOD detector.
   - Preserved all numerical threshold results exactly unchanged ($\tau \in [0.50, 0.95]$ sweeps, 37.50% rejection and 97.14% accepted accuracy at $\tau = 0.80$).

2. **Correction 2 — Soften 100% Internal Accuracy Claim:**
   - In Section V-A (`main.tex`), replaced:
     > *"As discussed in Section~\ref{sec:limitations}, this ceiling performance is facilitated by the image-level split on patch imagery from common preparation batches, which may contribute to the unusually high internal test performance."*
     
     with the cautious, verified statement:
     > *"This ceiling-level performance may be influenced by the image-level split, which can allow correlated patches or specimens to occur across partitions."*
   - In Section VI, Item 1 (Limitations), adjusted the text to state that image-level splitting permits correlated patches or specimens to potentially appear across partitions, removing unverified assertions regarding batch origins.
   - Kept all primary dataset results intact (15,000 images, 70:15:15 split, 2,250 test images, 100.00% accuracy, 1.0000 macro F1, 1.0000 macro ROC-AUC).

3. **Correction 3 — Fix Table VI Title:**
   - Updated the caption of Table VI in `main.tex` from:
     > `\caption{Comparative Architectural Analysis Across Evaluated Models on the Clinical Cohort Test Split ($N=57$)}`
     
     to:
     > `\caption{Comparative Architectural Analysis Across Evaluated Models}`
   - Preserved the `"Evaluation Dataset"` column distinguishing the Primary 15,000 Benchmark ($N=2,250$) from the Clinical Cohort Test Split ($N=57$).
   - Kept all metrics and values across all baseline models (ResNet-50, DenseNet-121, EfficientNet-B0, 4-layer CNN) exactly unchanged.

4. **Correction 4 — Verify Bibliographic Consistency:**
   - Conducted a strict bibliographic consistency review of all 20 references in `references.bib`.
   - Standardized author formatting and verified conference/journal metadata for Sertel, Kong, Boyer, and Catalyurek citations (`sertel2013detection`, `sertel2010computer`, `kong2010detection`, `sertel2012multi`).
   - Retained all 20 authentic citations without adding, removing, or replacing any references.
