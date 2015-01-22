<?php

// run WPCA on resource
if (isset($_GET['cl']) and $_GET['cl'])
    $chunk2 = ' yes';
else
    $chunk2 = '';  
if (isset($_GET['modulo']) and $_GET['modulo'])
    $chunk3 = ' ' . $_GET['modulo'];
else
    $chunk3 = ''; 

$command = escapeshellcmd('python3 wpca.py ' . $_GET['resource'] . $chunk2 . $chunk3);

$wpca = json_decode(shell_exec($command));

// delete 0s cutting lines
foreach ($wpca->vote_events as $k => $vote_event) {
    if  ($vote_event->cl_beta0 == 0)
        unset($wpca->vote_events[$k]);
}

// note: http://stackoverflow.com/questions/3629504/php-file-get-contents-very-slow-when-using-full-url
$context = stream_context_create(array('http' => array('header'=>'Connection: close\r\n')));

/* TEMPLATE */
// defaults
$defaults = [
    'width' => 600,
    'height' => 400
];
$current = [];
foreach ($defaults as $k => $default) {
    if (isset($_GET[$k]))
        $current[$k] = $_GET[$k];
    else
        $current[$k] = $default;
}

// p api
$parties = get_parties($wpca->people);

if (isset($_GET['party_set'])) {
    $chunk = '&set=' . $_GET['party_set'];
    $url = 'http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['SCRIPT_NAME']) . '/papi/?' . http_build_query(['parties' => $parties]) . $chunk;

    $r = json_decode(file_get_contents($url,false,$context));

    $abbr2row = [];

    foreach ($r->data as $row) {
        $abbr2row[$row->abbreviation] = $row;
    }
    $parties = $r->data;
    $wpca->people = add_attributes($wpca->people,$abbr2row);
} else {
    $wpca->people = add_attributes($wpca->people,[]);
}

// width and height
$absmax = absmax($wpca->people);
    //40: margins from scatterplot
if (2*$absmax['d1']/($current['width']-40) > 2*$absmax['d2']/($current['height']-40)) {
    $xmax = min(1.1,$absmax['d1']*1.1);
    $ymax = $xmax * ($current['height']-40)/($current['width']-40);
} else {
    $ymax = min(1.1,$absmax['d2']*1.1);
    $xmax = $ymax * ($current['width']-40)/($current['height']-40);
}

// rotation
if (isset($_GET['rotation'])) {
    $ar = explode('|',$_GET['rotation']);
    if (count($ar) == 1) {
        $ar[1] = 1;
        $ar[2] = 1;
    }
    $person = find_by_attr($ar[0],$wpca->people);
    if ($person) {
        $d1 = "wpca:d1";
        $d2 = "wpca:d2";
        if ($person->$d1 * $ar[1] < 0)
            $wpca = rotatex($wpca);
        if ($person->$d2 * $ar[2] < 0)
            $wpca = rotatey($wpca);
    }
}

//language / legend
if (isset($_GET['lang'])) {
    $lang = $_GET['lang'];
    $chunk = '&lang=' . $_GET['lang'];
} else {
    $chunk = '';
    $lang = 'en';
}
$url = 'http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['SCRIPT_NAME']) . '/lapi/?' . $chunk;
$r = json_decode(file_get_contents($url,false,$context));
$dim1 = $r->data->dim1;
$dim2 = $r->data->dim2;
    //possibly overwrite
if (isset($_GET['dim1']))
    $dim1 = $_GET['dim1'];
if (isset($_GET['dim2']))
    $dim2 = $_GET['dim2'];

// template
$html = file_get_contents('widget.tpl');
$replace = [
  '{_LINES}' => $wpca->vote_events,
  '{_PEOPLE}' => $wpca->people,
  '{_LABEL_DIM1}' => $dim1,
  '{_LABEL_DIM2}' => $dim2,
  '{_XMIN}' => -1*$xmax,
  '{_XMAX}' => $xmax,
  '{_YMIN}' => -1*$ymax,
  '{_YMAX}' => $ymax,
  '{_WIDTH}' => $current['width'],
  '{_HEIGHT}' => $current['height'],
  '{_LANG}' => $lang
];
foreach ($replace as $k => $r)
    $html = str_replace($k,json_encode($r),$html);
    
echo $html;



// FUNCTIONS
//rotate x
function rotatex($wpca) {
    $d1 = "wpca:d1";
    foreach($wpca->people as $person)
        $person->$d1 = -1*$person->$d1;
    foreach($wpca->vote_events as $vote_event)
        $vote_event->normal_x = -1*$vote_event->normal_x;
    return $wpca;
}

function rotatey($wpca) {
    $d2 = "wpca:d2";
    foreach($wpca->people as $person)
        $person->$d2 = -1*$person->$d2;
    foreach($wpca->vote_events as $vote_event)
        $vote_event->normal_y = -1*$vote_event->normal_y;
    return $wpca;
}

// find in object
function find_by_attr($needle,$array,$attr='id') {
    foreach($array as $struct) {
        if ($needle == $struct->$attr)
            return $struct;
    }
}

// abs max
function absmax($data) {
    $absmax = ['d1' => 0, 'd2' => 0];
    foreach ($data as $row) {
        $d1 = "wpca:d1";
        $d2 = "wpca:d2";
        if (abs($row->$d1) > $absmax['d1']) $absmax['d1'] = abs($row->$d1);
        if (abs($row->$d2) > $absmax['d2']) $absmax['d2'] = abs($row->$d2);
    }
    return $absmax;
}

//add attributes for people
function add_attributes($data,$abbr2row) {
    foreach ($data as $key => $row) {
        if (!isset($data[$key]->color)) {
            if (isset($abbr2row[$row->party]))
                $data[$key]->color = $abbr2row[$row->party]->color;
            else
                $data[$key]->color = 'gray';
        }    
    }
    return $data;
}

//select distinct parties
function get_parties ($data) {
    $list = [];
    foreach ($data as $row) {
        $list[$row->party] = $row->party;
    }
    $out = [];
    foreach ($list as $item)
        $out[] = $item;
    return $out;
}

?>
