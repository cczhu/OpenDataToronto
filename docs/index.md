<h1>Introduction</h1>

This repo houses my analysis work for the [Open Data Toronto meetup](https://www.meetup.com/opentoronto/).  All analysis was done in the Jupyter notebook (ipynb) environment.  A list of packages imported, and their versions, can be found in the root directory README.md.  The full analysis of each dataset can be viewed in the subfolders of the repo.  GitHub's ipynb viewer may not allow interactive plots to function, so I include [nbviewer](https://nbviewer.jupyter.org/) links to each project below.

You'll find short abstracts on all projects, listed in reverse chronological order, as well as a pretty plot generated during each project.  Additionally, I link to the associated meetup page of each project, where others have posted their analyses.

[Biggles](mydem0cracy_stdevvsmean.html) 

<h1>23/2/2017 - MyDem0cracy</h1>



<h1>24/11/2016 - Ontario Trillium Fund</h1>

[ipynb](https://nbviewer.jupyter.org/github/cczhu/OpenDataTorontoOTF/blob/master/Ontario%20Trillium%20Foundation%20Grants%20%28Open%20Data%20Toronto%202016-11-24%29.ipynb)
[Meetup Page](https://www.meetup.com/opentoronto/events/235293778/)

The [Ontario Trillium Foundation (OTF)](http://www.otf.ca/) is an agency of the Ontario provincial government that allocates more than $136 million annually in social/community program funding annually province-wide.  In accordance with the Ontario government's Open Data Directive, OTF provides data on grant applications over the last two decades on their [open data page](http://www.otf.ca/open).  I perform an exploratory analysis on this data, examining how aggregate, per-capita and per-project funding, and how it is divided into different project areas, have changed during that time.  I also break down funding for different populations served, and examine how funding is divided between Ontario's geographic regions.

<p align="center">
    <a href="images/otf_ontario.html">
    <img border="0" alt="OTF" src="otf_ontario.png" width="500" height="500">
    </a>
</p>

Figure: Per-capita OTF Spending in Ontario's census geographic regions.  Brighter and more orange colours represent higher funding per capita.  Populations are taken from 2011 census, and annual funding is averaged from its FY 2010 to 2016 values.  Click on the picture to go to the interactive version, where you can hover the mouse over a census area to see its name, population, number of OTF grants given per year, funding per year, median funding per project, and funding per capita (all OTF values are also averaged from FY 2010 to 2016).
