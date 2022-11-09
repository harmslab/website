# Lab Notebooks

Scientific results cannot be built on memories; they are built on documented, reproducible protocols and measurements.  The primary goal of your lab notebook is to document what you did, in detail sufficient to understand and reproduce your results.  It should be a *narrative* that describes what you did, why you did it, your actual results, and how you interpret them.

- If you didn’t document it, it didn’t happen.
- In two years, you’ll wish you had written more down.

#### Guidelines:

- Legible, in pen.  You can either use a normal lab notebook or build a loose-leaf notebook in a binder.
- Enter information **directly** into the notebook [no paper towels :)].
- Properly introduce **and** summarize each experiment.
- Tape in any external results (graph printouts, etc.)
- Note where any electronic files associated with experiment are stored.
- Include complete details of all first-time procedures, and cross-reference to page with full details for repeated procedures.
- Include calculations
- Keep up with the table of contents.
- Date and number each page.

## Electronic Data

### There are five main goals to keep in mind when dealing with electronic data in the Harms lab.

- **Backup:** Files should be backed up to cover everything from accidental deletion to destruction of the university.
- **Integrity:** Data files are the electronic equivalent of a lab notebook, meaning we need a tamper-resistant record of modifications.
- **Collaboration:** Lab data should be readable and immediately available to future and current lab members.
- **Archival readability:** Data needs to be readable by labs that do not possess any proprietary software used by our lab.
- **Publication:** All published experimental data should be readily available to requesting labs.

###Backup

- STUB

###File organization

A challenging aspect of lab data management is connecting the random files on a computer to their context in the real world (lab notebook, instrument settings, etc.). The following describes the best practices for four basic types of data we generate in the lab.

### Basic experimental data

- The directory containing experimental output should have the following format:
  YYYY-MM-DD_notebook-page_descriptive-name
- The raw experimental data should be exported into an appropriate non-proprietary, long-term file format.
- Each directory should have a clearly labeled summary file (image, text file/document, or graph). The summary file should be printed out and placed in the lab notebook.

####Example:

An ITC copper binding experiment done on September 20, 2013, cross-referenced to page 29 of MJH lab notebook #3. The final-summary.pdf file was printed out and placed in on that page in the lab notebook. The experimental directory would like something like:

2013-09-20_mjh3-29_hS100A5-copper-binding-itc/

instrument_output.itc –> raw experiment file
instrument_output.txt –> exported into ascii text file
integration.opj –> fitting file
final-summary.pdf –> exported pdf showing ITC trace

------

### **Large experimental/computational data**

This can be challenging to organize effectively. There has to be flexibility here because each project is different, but the important point is to think about someone trying to take apart the results without any other context. The following basic approach may be a useful starting point.

- Give each project a directory with a descriptive name
- At the top of the directory, include a README file that is populated as new work as done.
- Populate the directory with numbered sub-directories (and files) as you add them. This lets you organize your files in a linear, time-constructed, fashion.
- If possible, put the whole project under control of version control software (i.e. git).

**EXAMPLE:**

------

This is a subset of the files in a directory I used to generate a phylogeny of members of the S100 protein family. This process involves many different software packages, manual tweaks, and edits.

complete-s100-phylogeny/

README.txt
00_create-list-of-sequences/

00_initial-sequence-set.fasta
01_blast-results.txt
02_culled-sequence-set.fasta
03_reverse-blast.txt
04_final-sequence-set.fasta

01_alignment/

00_inital-alignment.fasta
00_inital-alignment.fasta.nex
01_refined-alignment.fasta
01_refined-alignment.fasta.nex
02_refined-remove-outliers.fasta
02_refined-remove-outliers.fasta.nex
03_final-alignment.fasta
03_final-alignment.phy

02_ initial-tree/

alignment.phy
phyml_spew.txt
phyml_tree.txt

03_try-different-models/

…

README.txt file might contain:

2013-09-26

Goal: create a detailed ML phylogeny of the S100 family, starting from scratch.

00_create-list-of-sequences (2013-09-26): use the human family members as a blast query, refine the output by minimizing redundant hits, and then check each ortholog call by reverse-blast.

01_alignment (2013-09-30): create an alignment of the sequences using msaprobs, followed my manual refinement in Mesquite.

02_initial-tree (2013-09-30): create an initial tree using phyml. Used LG+gamma8 model, SPR moves.

03_try-different-models (2013-10-04): …

------

### **Software**

Stub: version control with git

### File formats

Stub: All data should be converted into common, open spec file formats.

### **Publication**

The first author of each paper should compile a set of directories for each data figure and table in the manuscript, containing the raw data (in open format), as well as the analysis done. By compiling this as the paper is being written, we will guarantee that we have the data to support our conclusions, as well as have the information in easily accessible form for future consultation and/or sharing with other labs.



# Stocks
