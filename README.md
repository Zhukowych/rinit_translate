# rinit_translate
<p>Script for creating translation table from tables in database. In this script finds in database's tables columns with language identiffers, such as "uk" either "ru"
and creates unique translations. In this versions only 'ua' amd 'ru' are maintained</p>
<h3>Usage</h3>
See <a href="https://github.com/Zhukowych/rinit_translate/blob/main/requirements.txt">requirements.txt</a> and install python packages listed there.
<br>
<code>python3 main.py -table_name '<table to export>' [-import_tables '<tables to import>'] [--all-tables] [--unaccept_eng]</code><br>
<ul>
  <li><code>-table_name</code> - name of table, to whitch will export translations</li>
  <li><code>-import_tables '<tables to import>'</code> - names of tables, from whitch will import data</li>
  <li><code>---all-tables</code> - import data from all tables</li>
  <li><code>unaccept_eng</code> - unaccept tranlations, which contain of end and other unaccept symbols</li>
</ul>
<p><code>---all-tables</code> or <code>-import_tables '<tables to import>'</code> may be provided. In start of script run table with name 'table to export' will be  created and if table with that name was in database, all data from is will be deleted</p>
