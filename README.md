# CPI Data

Use Python to download Pull CPI Data from BLS (https://download.bls.gov/pub/time.series/cu/)

Inputs:
- none

Output: 
- several .txt files from above, with 'cpi_' as a prefix
- one .csv file with the relevant .txt files combined using pandas

TODO:
- Use the area_name to look at CPI regionally
- Pull data from https://www.bls.gov/cpi/tables/supplemental-files/ to identify weights based on CPI component
- Create treemap with sizing based on weights by CPI component (shaded based on increases/decreases)
- Create waterfall chart by CPI component/category to show YoY change in price
