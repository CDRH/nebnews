Update Essay
==========

Essays are stored in the database in html form.  If you have access to phpMyAdmin, the best way to go about it would simply be to open that up, go to the core_essay table, and start editing away.

New Essay
============

This is a bit trickier.  Due to there being so few essays, rather than try to fix the ingestion script for Nebraska's purposes, the essays were simply added by hand.  You will need to use the core_essay table to store the essay itself and then core_essay_title table to link the essay to one or more newspapers.  You can refer here for more help:  [Linking Essays to Titles](https://docs.google.com/document/d/1_QdtUb9FgrHlBupFM6kCol6TBTG6Xa5brhbh31w-fjU/edit#heading=h.i2jzq1boumcg)

