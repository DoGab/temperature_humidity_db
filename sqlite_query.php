<?php

  class MyDB extends SQLite3
  {
    function __construct()
    {
      $this->open('/home/pi/databases/temperaturedb');
    }
  }

  $db = new MyDB();
  if(!$db) die($db->lastErrorMsg());

  $sql_query = "select * from sensordata";
  $result = $db->query($sql_query);

  if (!$result) die("Cannot execute query.");
  while ($row = $result->fetchArray()) {
    var_dump($row);
  }
  #echo json_encode($result);
  
?>
