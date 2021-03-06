<?php

  class MyDB extends SQLite3
  {
    function __construct()
    {
      $this->open('/opt/thermvis/database/thermvisdb');
    }
  }

  $json = $_POST['hours'];
  $data = json_decode($json);
  $hours = $data * 12;

  $db = new MyDB();
  if(!$db) die($db->lastErrorMsg());

  $sql_query = "select * from (select * from sensordata order by timestamp desc limit " . $hours . ") order by timestamp asc;";
  $result = $db->query($sql_query);

  if (!$result) die("Cannot execute query.");
  $result_array = array();
  while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    #var_dump($row);
    $result_array[] = $row;
  }
  echo json_encode($result_array);
  
?>
