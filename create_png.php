<?php

$filenamesvg = 'cache/svg/' . $_POST['url'] .'.svg';

$cache_life = 600;  //caching time, in seconds

$fmtime = filemtime($filenamesvg);
print_r($_POST['nocache']);
if ((!$fmtime or (time() - $fmtime >= $cache_life)) or ((isset($_POST['nocache'])) and $_POST['nocache'])) {
    file_put_contents($filenamesvg,$_POST['svg']);
    
    $com = 'inkscape -z -e cache/png/' . $_POST['url'].'.png cache/svg/' .  $_POST['url'].'.svg';

    exec($com);
}

#$fsvg = fopen('cache/svg/' . $_POST['url'].'.svg','w');
#fwrite($fsvg,$_POST['svg']);
#fclose($fsvg);



?>
