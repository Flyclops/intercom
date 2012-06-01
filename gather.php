<?php

$members=array(
   "1234"=>array(
      "name"=>"Alex Hillman")
  ,"2345"=>array(
      "name"=>"Adam Teterus")
  ,"3456"=>array(
      "name"=>"Geoff DiMasi")
  ,"9999"=>array(
      "name"=>"Johnny Bilotta")
  ,"9876"=>array(
      "name"=>"Parker Whitney"
     ,"tone"=>"http://phone.indyhall.org/voice/Parker1.mp3")
);

function get_member_by_code($code) {
  global $members;
  if (array_key_exists($code, $members)) {
    $member = $members[$code];
    return $member;
  }
  
  return null;
}

function get_member_tone($member) {
  if (array_key_exists('tone', $member)) {
    return $member['tone'];
  } else {
    return "http://idisk.s3.amazonaws.com/tmp/9.wav";
  }
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";

$digits = $_REQUEST['Digits'];
$member = get_member_by_code($digits);

if ($member != null) {
  $tone = get_member_tone($member);
  ?>
  <Response>
    <Play><?php echo $tone; ?></Play>
  </Response>
  <?php
  die;
}
elseif ($digits == '0') {
  ?>
  <Response>
    <Play>http://phone.indyhall.org/voice/FrontDesk1.mp3</Play>
    <Dial>267-702-4865</Dial>
  </Response>
  <?php
  die;
}
else {
?>
  <Response>
    <Gather action="http://phone.indyhall.org/gather.php" method="POST">
      <Play>http://phone.indyhall.org/voice/Invalid3.mp3</Play>
      <Play>http://phone.indyhall.org/voice/Guest4.mp3</Play>
    </Gather>
  </Response>
<?php
}
?>
