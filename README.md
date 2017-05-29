# Widget: W-PCA
Widget for calculation of WPCA and creation of its chart, possibly with the cutting lines.

![picture](https://raw.githubusercontent.com/KohoVolit/widget-wpca/master/examples/scatterplot-chart.png "Example")

[WPCA procedure (in R) is described here](https://gist.github.com/michalskop/8514867)

The visualization is a [D3 reusable chart](http://bost.ocks.org/mike/chart/), which may be used separately.

**Important note**: The calculation takes long time, therefore the widget should be cached.

## Requirements
Python3  
R: (needs to be set correct path in `wpca_script.r`, line `library("reshape2", ...` ;TBD**)  
PHP

## Parameters
### resource (required)
Resource needs to be a `json` list, consisting of 3 objects: `people`, `vote_events`, `votes`.  
`people` have *required* attributes: `name`, `party`, `id`;  
`vote_events` have *required* attributes: `id`, `motion:name`, `start_date`;  
`votes` have *required* attributes: `voter_id`, `vote_event_id`, `option`;  

Another attribute of `people` are *semi-optional* (they are required unless `party_set` is set): `color`

Example of resource:
```json
{
"votes": [
  {"voter_id": "1", "option": "yes", "vote_event_id": "13"},
  {"voter_id": "2", "option": "abstain", "vote_event_id": "13"},
  ...],
"vote_events": [
  {"motion:name": "Motion 1", "start_date": "2011-11-04", "id": "13"}, 
  ...],
"people": [
  {"name": "Michelle", "party": "Fairies", "id": "1"},
  ...]
}
```

### lang (optional)
Language [ISO 639-1 code](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). The language file (e.g.,`cs.json`) needs to exist in `lapi/` directory.

Default: `en`

Example of lang: `cs`

### party_set (optional)
Name of set of parties (file with parties' information). The party set file (e.g., `cz.json`) needs to exist in `/papi` directory.

Default: none

Example of party_set: `cz`

Note: either `party_set` is required, or the resource must contain `color` for each person.

### width (optional)
Width of the visualization in pixels.

Default: `600`

### height (optional)
Height of the visualization in pixels.

Default: `400`

### cl (optional)
Indicates if cutting lines shall be computed and displayed (e.g., `cl=1`)

Default: `false`

### modulo (optional)
If the cutting lines shall be computed (i.e., `cl=1`), only each *modulo*-th cutting line is computed and displayed.

Default: `1`

### rotation (optional)
Sets rotation of the final chart. It is list of 3 parameters divided by `|`: *voter_id*, *position in the 1st dimension* (right is 1, left is -1), *position in the 2nd dimension* (up is 1, down is -1).  
The 2nd and 3rd parameters may be ommited (defaults to `1|1`).

Default: no rotation

Examples: `rotation=2|-1|1` (the voter with 2 will be left and up) , `rotation=2` (equals to `rotation=2|1|1`)

### dim1, dim2 (optional)
Sets names for axes

Default: depending on `lang` (*Dimension 1* and *Dimension 2* in English)

## Examples
### Example resource
There is an example of helper Python script (`load_datapackage.cgi`) converting `datapackage` into required json resource in the `/examples/cgi` directory. (This script usually needs to be placed in `/var/www/cgi-bin/` directory.)

The example of `datapackage` with 3 `csv` file is also in `/examples` directory.

### Example calling
```url
widget.php?resource=http://localhost/cgi-bin/wpca/load_datapackage.cgi%3Fdatapackage%3Dhttp%3A%2F%2Flocalhost%2Fmichal%2Fproject%2Fwidget-wpca%2Fexamples%2Fdatapackage.json
&lang=en
&party_set=cz
&width=650
&height=600
&cl=1
&modulo=10
&rotation=123|-1|1
&dim1=LEFT-RIGHT
&dim2=LIB-CON
```
