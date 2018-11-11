<h1>Ontario Trillium Foundation Grants 1999 - 2016</h1>

[Analysis ipynb](https://nbviewer.jupyter.org/github/cczhu/OpenDataToronto/blob/master/OTF/Ontario%20Trillium%20Foundation%20Grants%20%28Open%20Data%20Toronto%202016-11-24%29.ipynb)<br/>
[Meetup Page](https://www.meetup.com/opentoronto/events/235293778/)

<h3>Requirements</h3>

bokeh==0.12.3 <br>
geopy==1.11.0 <br>
matplotlib==1.5.3 <br>
numpy==1.12.0 <br>
pandas==0.19.1 <br>
plotly==1.12.12 <br>
scikit-learn==0.18.1 <br>
scipy==0.18.1 <br>
seaborn==0.7.1

<h3>Datasets</h3>

The OTF data comes from the following files:

    Ontario Trillium Fund. No date. Grants for the period between 1999 to 2015 (database).
    http://www.otf.ca/sites/default/files/otf_granting_data_fiscal_year_2000-2015_20150717.csv (accessed November 22nd, 2016).

    Ontario Trillium Fund. No date. Grants for the period between 2015 to 2016 (database).
    http://www.otf.ca/sites/default/files/otf_granting_data_since_april_1_2015.csv (accessed November 22nd, 2016).

The geographic regions used in these files is related to the Statistics Canada census regions with this file:

    Ontario Trillium Fund. No date.  OTF Catchment area census division (database). 
    http://www.otf.ca/sites/default/files/otf_catchment_area-census_division_concordance_file.csv (accessed November 23rd, 2016).

Their boundaries are given by:

    Statistics Canada. No date. Boundary files (database). 
    https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2011-eng.cfm (accessed December 25th, 2016).

The file inflation.txt is derived from the Bank of Canada's inflation calculator.

    Bank of Canada. No date. Inflation Calculator (database). 
    http://www.bankofcanada.ca/rates/related/inflation-calculator/ (acessed November 24th, 2016).

Other data in this repo are derived from Statistics Canada's archives:

    Statistics Canada. No date. Table 051-0005 - Estimates of population, Canada, provinces and territories, quarterly (persons), 
    CANSIM (database). http://www5.statcan.gc.ca/cansim/a26?lang=eng&id=510005 (accessed November 24th, 2016).

    Statistics Canada. No date. Population and Dwelling Count Highlight Tables, 2011 Census (database). 
    http://www12.statcan.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/Table-Tableau.cfm?
    LANG=Eng&T=702&SR=1&S=51&O=A&RPP=9999&PR=35&CMA=0#symbol-dagger (acessed November 24th, 2016).
