Batches
==========

The Nebraska Newspapers projects has largely the same information that the Chronicling America website contains.  There are a few exceptions.  The below is a list of batches that the Nebraska Newspapers has that the LoC does not.  DN = Daily Nebraskan

- batch_nbu_aristotle_ver01  (DN)
- batch_nbu_bravo_ver01  (DN, Hesperian)
- batch_nbu_czech_ver01  (Ozvêna západu, Prítel lidu, Wilberské listy)
- batch_nbu_DailyNebraskan_ver01  (DN)
- batch_nbu_echo_ver01  (DN)
- batch_pm@_delivery1_ver01  (plattsmouth)
- batch_pm@_delivery2_ver01  (plattsmouth)
- batch_pm@_deliver3_ver01  (plattsmouth)

The lccns for the following batches were modified:

- batch_nbu_alpha_ver01 (using sn96080312)
- batch_nbu_bravo_ver01 (changed sn94080311 to sn96080312)
- batch_nbu_eisley_ver01  (see below)

Other Changes
----------

- @pm manually added as an awardee in order to process plattsmouth batches
- Titles altered for capitalization
- Ozvěna západu title corrected (symbol ě instead of é)
- Date correction for Daily Nebraskan issue that claims it was made in the 18th century

nbu_eisley
-----------

Eisley was a problem and will continue to be a problem because it was scattered over three different places in the network drives that UNL holds.  While attempting to assemble it, it was discovered that our eisley has more information than the LoC's eisley.  Also, we had to change many lccns in order to match the correct lccns in the LoC.  Sadly, the Hemingford Herald is still being considered the Alliance Herald because there is no unique lccn for the HH.

Redownloading
-------------

We had to redownload batch_nbu_fairbury_ver01 because the version we had was missing directories and files.

If you need to re-download a batch from the LoC, you can get it with the following command (sub in the name of the batch):

```
wget --recursive --no-host-directories --cut-dirs 1 --reject index.html* --include-directories /data/batches/batch_nbu_abbott_ver01/ http://chroniclingamerica.loc.gov/data/batches/batch_nbu_abbott_ver01/
```
