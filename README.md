# Family_Tree
Python code to create a Family Tree from collected pictures



How to use:

1. Create a CSV file will following columns
   name - Name of the Person - Mandatory
   alias - Alias or a.k.a (Also known as) - Optional
   gender - Gender of the person - Mndatory
   dob - Date of birth - Optional
   dod - Date of Death - Optioanl
   mother_name - Mother's name (must have person record for the mother in the CSV)
   father_name - Father's name (must have person record for the father in the CSV)
   spouse_name - Spouse name (must have person record for the spouse in the CSV)
   dom - Date of marriage (Optional)
2. Store the images in the images folder, see sample files (non-thumbnail files)
3. To run this program execute following on command prompt
Syntax:
  python family_tree.py <name of csv> <Graph Title>
Example:
  python family_tree.py homer_family_tree.csv "Simpson's Family"

This script creates the thumbnails to achieve size consistancy for the images int he final output

See homer_family_tree.dot.pdf, is the sample output
Output PDF file will be created using the CSV file name
