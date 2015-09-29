Add a Language
==============

(This documentation is incomplete, it only has the solr config portion of the setup required)

Solr Config
-----------

Let's add Czech!  Your solr core is likely located at `/opt/solr/solr/collection1` if you followed the installation instructions exactly.  Otherwise, navigate to where your core is located.

Verify that the language stopwords file exists in `/opt/solr/solr/collection1/conf/lang`.  Now open up `/opt/solr/solr/collection1/conf/schema.xml` and add the following fieldType:

```
    <fieldType name="text_cze" class="solr.TextField">
      <analyzer>
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.ElisionFilterFactory" ignoreCase="true"/>
        <filter class="solr.ASCIIFoldingFilterFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="lang/stopwords_cz.txt" enablePositionIncrements="true"/>
        <filter class="solr.WordDelimiterFilterFactory"/>
        <filter class="solr.CzechStemFilterFactory"/>
        <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
      </analyzer>
    </fieldType>
```

You will probably want to add that where the other fieldTypes are being defined, like "text_eng" and "text_fre".  Now, go ahead and add another field called "ocr_cze" where all the other fields are defined:

```
    <field name="ocr_cze" type="text_cz" indexed="true" stored="true" required="false" multiValued="false"/>
```

