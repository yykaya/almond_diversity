#!/usr/bin/env python3
import sys
input_filename = "SV_output_geno_final_all.txt" 
prunus_samples = ["P_arabica", "P_argentea", "P_webbii"] 
alt_genotypes = {"0/1", "1/1", "1/0"}
output_handles = { sample: open(f"{sample}_unique_SV_regions.txt", "w") for sample in prunus_samples }

with open(input_filename, "r") as infile:
    header_line = infile.readline().rstrip("\n")
    header_fields = header_line.split("\t")
    
    # Determine the indices for key columns.
    # If an "SV" column exists, use it; otherwise, we will assign sequential IDs.
    try:
        sv_idx = header_fields.index("SV")
    except ValueError:
        sv_idx = None
    chrom_idx = header_fields.index("Chromosome")
    pos_idx = header_fields.index("Position")
    
    # get indices for each prunus sample.
    prunus_indices = {}
    for sample in prunus_samples:
        try:
            prunus_indices[sample] = header_fields.index(sample)
        except ValueError:
            sys.exit(f"Error: {sample} not found in header.")
    
     
    header_out = "\t".join(["SV", "Chromosome", "Position"]) + "\n"
    for sample in prunus_samples:
        output_handles[sample].write(header_out)
    
    
    sv_counter = 1
    
 
    for line in infile:
        line = line.rstrip("\n")
        fields = line.split("\t")
        
         
        if sv_idx is not None:
            sv_id = fields[sv_idx]
        else:
            sv_id = f"SV{sv_counter}"
            sv_counter += 1
        
         
        chrom = fields[chrom_idx]
        if chrom.startswith("Chr"):
            chrom = chrom.replace("Chr", "")
        pos = fields[pos_idx]
        
         
        for sample in prunus_samples:
            sample_idx = prunus_indices[sample]
            cell = fields[sample_idx]
            gt = cell.split(":")[0]
            if gt in alt_genotypes:
                 
                unique = True
                for other in prunus_samples:
                    if other == sample:
                        continue
                    other_idx = prunus_indices[other]
                    other_cell = fields[other_idx]
                    other_gt = other_cell.split(":")[0]
                    if other_gt in alt_genotypes:
                        unique = False
                        break
                if unique:
                    out_line = "\t".join([sv_id, chrom, pos]) + "\n"
                    output_handles[sample].write(out_line)

 
for sample in prunus_samples:
    output_handles[sample].close()

print("extraction of unique prunus SV regions complete.")
