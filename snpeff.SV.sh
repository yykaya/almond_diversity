snpEff_jar="/u/ykaya/snpEff/snpEff.jar"

memory_allocation="16g"


vcf_files=("China_pd.vcf" "France_languedoc.vcf" "Pakistan_pd2.vcf" "P_argentea.SVs.vcf" "P_webbii.SVs.vcf" "Ukraine_pd.vcf" "Iran_pd.vcf" "P_arabica.SVs.vcf" "P_dulcis_TR_SV.vcf" "Spain_Marcona_pd1.vcf" "USA_Nonpareil_pd.vcf")


for vcf_file in "${vcf_files[@]}"; do
    #extract the basename of the file (without extension)
    base_name=$(basename "$vcf_file" .vcf)

    
    mkdir -p "$base_name"

     
    cp "$vcf_file" "$base_name/"

    
    cd "$base_name" || exit

    #run snpEff and output the annotated VCF in the current directory
    java -Xmx$memory_allocation -jar $snpEff_jar Prunus_dulcis2 -v "$vcf_file" > "${base_name}_ano.vcf"

    
    echo "Annotation completed for $vcf_file and saved as ${base_name}/${base_name}_ano.vcf"

 
    cd ..

done
