#!/usr/bin/env python3
import sys
input_filename = "SV_output.txt"
output_filename = "wild_prunus_only.txt"
alt_genotypes = {"0/1", "1/1", "1/0"}
wild_samples = ["P_arabica", "P_argentea", "P_webbii"]

with open(input_filename, "r") as infile, open(output_filename, "w") as outfile:
    header = infile.readline().rstrip("\n")
    fields = header.split("\t")
    
    
    try:
        sv_idx = fields.index("SV")
    except ValueError:
        sv_idx = None
    chrom_idx = fields.index("Chromosome")
    pos_idx = fields.index("Position")
    
    
    wild_indices = {}
    for sample in wild_samples:
        try:
            wild_indices[sample] = fields.index(sample)
        except ValueError:
            sys.exit(f"Error: {sample} not found in header.")
    
    
    out_header = ["SV", "Chromosome", "Position"] + wild_samples
    outfile.write("\t".join(out_header) + "\n")
    
    sv_counter = 1   
    
    for line in infile:
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split("\t")
        
        
        if sv_idx is not None:
            sv_id = parts[sv_idx]
        else:
            sv_id = f"SV{sv_counter}"
            sv_counter += 1
        
        chrom = parts[chrom_idx]
        pos = parts[pos_idx]
        
        
        wild_calls = {}
        has_alt = False
        for sample, idx in wild_indices.items():
            cell = parts[idx]
            # Get genotype (first field before colon)
            gt = cell.split(":")[0]
            wild_calls[sample] = gt
            if gt in alt_genotypes:
                has_alt = True
        
         
        if has_alt:
            out_line = [sv_id, chrom, pos] + [wild_calls[sample] for sample in wild_samples]
            outfile.write("\t".join(out_line) + "\n")

print(f"well, extraction complete.. output written to {output_filename}")
