# Exporting

In the tool database window in VCarve, select one of the top-level "folders"
of tools, and click the save button. This will yield a `.vtdb` file. When
checking that into git, run the following to convert it to text format too:

```
echo .dump | sqlite3 vcarve-tools-imperial.vtdb > vcarve-tools-imperial.vtdb.sql
echo .dump | sqlite3 vcarve-tools-imperial.vtdb > vcarve-tools-metric.vtdb.sql
```

# Importing

TODO.
