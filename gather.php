<?php

$members=array(
   "1234"=>"Alex Hillman"
  ,"2345"=>"Adam Teterus"
  ,"3456"=>"Geoff DiMasi"
  ,"9999"=>"Johnny Bilotta"
  ,"9876"=>"Parker Whitney"
);

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
if(array_key_exists($_REQUEST['Digits'], $members)){
  ?>
  <Response>
    <?  if($_REQUEST['Digits'] == '9876'){
          ?>
          <Play>http://phone.indyhall.org/voice/Parker1.mp3</Play>
          <?
        }
    ?>
    <Play>http://idisk.s3.amazonaws.com/tmp/9.wav</Play>
  </Response>
  <?php
  die;
}
elseif($_REQUEST['Digits'] == '0'){
  ?>
  <Response>
    <Play>http://phone.indyhall.org/voice/FrontDesk1.mp3</Play>
    <Dial>267-702-4865</Dial>
  </Response>
  <?php
  die;
}
else{
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