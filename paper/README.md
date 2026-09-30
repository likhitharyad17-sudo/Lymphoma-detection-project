# IEEE Conference Paper: Attention-Augmented Residual Deep Learning Framework for Lymphoma Classification

This repository contains the complete, publication-ready IEEE conference LaTeX project for the research manuscript:

**"Attention-Augmented Residual Deep Learning Framework for Histopathological Lymphoma Subtype Classification and Screening"**

---

## Authors & Affiliation
- **Bhuvanesh A U**$^1$, **Likith Arya D**$^1$, **Monisha K P**$^1$, **Manthan Nayak**$^1$, and **Mrs. Sindhu K S**$^2$
- $^1$Department of Information Science and Engineering, Malnad College of Engineering, Hassan, Karnataka, India
- $^2$Assistant Professor, Department of Information Science and Engineering, Malnad College of Engineering, Hassan, Karnataka, India

---

## Directory Structure
```
paper/
│
├── main.tex                  # Primary IEEEtran LaTeX manuscript
├── references.bib            # Complete, verified BibTeX citations
├── figures/                  # Publication figures (PDF vector & PNG)
│   ├── fig1_framework.pdf / .png
│   ├── fig2_architecture.pdf / .png
│   ├── fig3_dataset_distribution.pdf / .png
│   ├── fig4_training_curves.pdf / .png
│   ├── fig5_confusion_matrix.pdf / .png
│   ├── fig6_roc_curves.pdf / .png
│   ├── fig7_gradcam.pdf / .png
│   └── fig8_ablation_threshold.pdf / .png
├── PROJECT_REPORT.md         # Comprehensive project summary & verified metrics
└── README.md                 # Instructions for Overleaf compilation
```

---

## How to Compile in Overleaf

1. **Compress the `paper/` folder into a `.zip` archive**:
   - Ensure `main.tex`, `references.bib`, and the `figures/` directory are at the top level of the archive.
2. **Upload to Overleaf**:
   - Go to [Overleaf](https://www.overleaf.com/).
   - Click **New Project** $\rightarrow$ **Upload Project**.
   - Select your `.zip` archive.
3. **Compiler Settings**:
   - Set the compiler to **pdfLaTeX** or **XeLaTeX**.
   - Set the main document to `main.tex`.
   - Click **Recompile**.
4. The output PDF will compile cleanly with two-column IEEE format, all 8 figures, 6 tables, mathematical formulations, and complete citations.

---

## How to Compile Locally (Command Line)
If you have TeX Live or MiKTeX installed:
```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
