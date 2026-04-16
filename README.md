Phylogenetic Analysis Pipeline (Python-Based Integrated Workflow)
================================================================

Overview
--------
This repository provides an automated and reproducible pipeline for phylogenetic analysis. The pipeline integrates multiple stages of analysis, including sequence retrieval, multiple sequence alignment (MSA), phylogenetic tree inference, visualization, and statistical comparison of alternative tree topologies.

The primary goal of this framework is to enable a consistent and systematic workflow for comparing different alignment and inference strategies within a single computational environment.


Features
--------
• End-to-end phylogenetic workflow in Python  
• Multiple Sequence Alignment tools:
  - MAFFT  
  - MUSCLE  
  - ClustalW  

• Tree inference methods:
  - Neighbor-Joining (NJ)  
  - UPGMA  
  - Maximum Likelihood (IQ-TREE)  
  - Maximum Parsimony (PHYLIP DNAPARS)  

• Tree visualization (PNG format)  

• Tree comparison metrics:
  - Robinson-Foulds (RF) distance  
  - Normalized RF distance  
  - Branch length correlation  

• Statistical evaluation:
  - Approximately Unbiased (AU) test  
  - Kishino-Hasegawa (KH) test  
  - Shimodaira-Hasegawa (SH) test  

• Resume capability for long-running experiments  


Repository Structure
--------------------
PhyloPipeline/
│
├── install_dependencies.txt
│   Install all required dependencies
│
├── fetch_sequences_ncbi.py
│   Generate FASTA input data from NCBI
│
├── phylo_pipeline.py
│   Main pipeline script
│
├── README.md
│   Documentation



Installation
------------
Step 1: Clone the repository

    git clone <your-repo-link>
    cd PhyloPipeline

Step 2: Install dependencies

    install_dependencies.txt


Usage
-----
Step 1: Generate input FASTA file (optional)

    python fetch_sequences_ncbi.py

Provide:
- Organism name  
- Gene name  
- Number of species  

Output: Phylogeny-safe FASTA file


Step 2: Run the pipeline

    python phylo_pipeline.py

You will be prompted to:
- Provide input FASTA file path  
- Select sequence type (DNA/Protein)  
- Choose alignment method(s)  
- Choose tree inference method(s)  
- Enable/disable full combinational analysis  
- Enable/disable visualization  


Output
------
The pipeline generates:

- Aligned sequence files  
- Phylogenetic trees (Newick format)  
- Tree visualizations (PNG images)  
- Pairwise tree comparison results  
- Statistical test outputs (AU, KH, SH)  

All results are stored in a dedicated output directory created for each run.


Reproducibility
---------------
Reproducibility is ensured through:

- install_dependencies.txt for dependency installation  
- fetch_sequences_ncbi.py for input generation  
- Supplementary alignment datasets  
- Deterministic re-execution using identical inputs  


Scope and Intended Usage
------------------------
This pipeline is intended for users familiar with computational environments, including graduate students, bioinformaticians, and researchers performing phylogenetic analysis.

It is particularly useful for systematically comparing different alignment and tree inference strategies within a unified workflow.

The framework complements systems such as Galaxy by providing a command-line-based, scriptable environment focused on automation and comparative analysis, including statistical evaluation of alternative phylogenetic trees.


Limitations
-----------
- Supports a selected set of alignment and inference methods  
- Command-line based (no graphical interface)  
- Performance depends on dataset size and system configuration  
- Further benchmarking on large-scale datasets can extend validation  
