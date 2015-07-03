<?php

//calculate WPCA for resource
$wpca = wpca();

//removes 0 cutting lines (not cutting)
remove_zero_cl($wpca);

// note: http://stackoverflow.com/questions/3629504/php-file-get-contents-very-slow-when-using-full-url
$context = stream_context_create(array('http' => array('header'=>'Connection: close\r\n')));

//update defaults
$current = update_defaults();

// add colors from groups
colors($wpca,$current);

//print_r($wpca);//die();

//calculate maxima of axes
$xymax = maxima($wpca,$current);




/* TEMPLATE */
    // template
    $html = file_get_contents('widget.tpl');

    $replace_jsonized = [
      '{_LINES}' => $wpca->vote_events,
      '{_PEOPLE}' => $wpca->voters,
      '{_LABEL_DIM1}' => 'dim1',
      '{_LABEL_DIM2}' => 'dim2',
      '{_XMIN}' => -1*$xymax['x'],
      '{_XMAX}' => $xymax['x'],
      '{_YMIN}' => -1*$xymax['y'],
      '{_YMAX}' => $xymax['y'],
      '{_WIDTH}' => $current['width'],
      '{_HEIGHT}' => $current['height'],
      '{_LANG}' => 'en'
    ];

    foreach ($replace_jsonized as $k => $r)
        $html = str_replace($k,json_encode($r),$html);

    $replace = [
#      '{_WIDGET_PICTURE}' => $widget_picture,
      '{_OG_IMAGE}' => '',//$og_image,
      '{_OG_URL}' => ''//$og_url,
    ];
    foreach ($replace as $k => $r)
        $html = str_replace($k,$r,$html);
        
    echo $html;


// calculate maxima of axes
function maxima($wpca,$current) {
    $absmax = absmax($wpca->voters);
        //40: margins from scatterplot
    if (2*$absmax['d1']/($current['width']-40) > 2*$absmax['d2']/($current['height']-40)) {
        $xmax = min(1.1,$absmax['d1']*1.1);
        $ymax = $xmax * ($current['height']-40)/($current['width']-40);
    } else {
        $ymax = min(1.1,$absmax['d2']*1.1);
        $xmax = $ymax * ($current['width']-40)/($current['height']-40);
    } 
    return ['x' => $xmax, 'y' => $ymax];  
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

// add colors from groups
function colors($wpca,$current) {
    if (isset($_GET['color']) and $_GET['color']) {
        $ps = csv_to_array('colors/' . $_GET['color'] . '.csv');
        //reorder
        $parties = [];
        foreach ($ps as $p) {
            $parties[$p['name']] = $p;
        }
    } else {
        $parties = [];
    }
    foreach ($wpca->voters as $voter) {
        if (!isset($voter->color)) {
            if (isset($parties[$voter->{'group:name'}]))
                $voter->color = $parties[$voter->{'group:name'}]['color'];
            else {
                $rancol = random_color();
                $parties[$voter->{'group:name'}] = ['color' => $rancol];
                $voter->color = $rancol;
            }
        }
    }
}

// random color
// https://css-tricks.com/snippets/php/random-hex-color/
function random_color() {
    $rand = array('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f');
    $color = '#'.$rand[rand(0,15)].$rand[rand(0,15)].$rand[rand(0,15)].$rand[rand(0,15)].$rand[rand(0,15)].$rand[rand(0,15)];
    return $color;
}

// rewrites defaults
function update_defaults() {
    $defaults = defaults();
    $current = [];
    foreach ($defaults as $k => $default) {
        if (isset($_GET[$k]))
            $current[$k] = $_GET[$k];
        else
            $current[$k] = $default;
    }
    return $current;
}

// get defaults
function defaults() {
    $defaults = [
        'width' => 600,
        'height' => 400,
        'colors' => 'mx',
        'dim1' => 'Dim 1',
        'dim2' => 'Dim 2',
    ]; 
    return $defaults;   
}


// deletes 0s cutting lines
function remove_zero_cl ($wpca) {
    foreach ($wpca->vote_events as $k => $vote_event) {
        if  ($vote_event->cl_beta0 == 0)
            unset($wpca->vote_events[$k]);
    }
}


//calculates WPCA
function wpca() {
    $command = command();
    $wpca = json_decode(shell_exec($command));
    return $wpca; 
}

// creates shell command to calculate WPCA
function command() {
    $command = 'python3 calculate_wpca.py ' . urldecode($_GET['resource']);
    if (isset($_GET['cl']) and $_GET['cl']) {
        $chunk2 = ' yes';
        if (isset($_GET['nth']) and $_GET['nth'])
            $chunk3 = ' ' . $_GET['nth'];
        else
            $chunk3 = ' 1'; 
    }
    else {
        $chunk2 = ' no';  
        $chunk3 = ' 1'; 
    } 
    $chunk4 = ' 2';
    $chunk5 = ' most';
    $command .= $chunk2 . $chunk3 . $chunk4 . $chunk5;  
    return escapeshellcmd($command);
}

// reads csv file into associative array
// https://gist.github.com/jaywilliams/385876
function csv_to_array($filename='', $delimiter=',') {
	if(!file_exists($filename) || !is_readable($filename))
		return FALSE;
	$header = NULL;
	$data = array();
	if (($handle = fopen($filename, 'r')) !== FALSE)
	{
		while (($row = fgetcsv($handle, 1000, $delimiter)) !== FALSE)
		{
			if(!$header)
				$header = $row;
			else
				$data[] = array_combine($header, $row);
		}
		fclose($handle);
	}
	return $data;
}


