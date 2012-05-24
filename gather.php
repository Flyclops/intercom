<?php

$members=array(
   "1234"=>"Alex Hillman"
  ,"2345"=>"Adam Teterus"
  ,"3456"=>"Geoff DiMasi"
  ,"9999"=>"Johnny Bilotta"
);

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
if(array_key_exists($_REQUEST['Digits'], $members)){
  ?>
  <Response>
      <Say>Hello, <?php echo $members[$_REQUEST['Digits']] ?></Say>
      <Play>http://idisk.s3.amazonaws.com/tmp/9.wav</Play>
  </Response>
  <?php
  die;
}
elseif($_REQUEST['Digits'] == '0'){
  ?>
  <Response>
    <Say>Connecting you to Adam</Say>
    <Dial>267-702-4865</Dial>
  </Response>
  <?php
  die;
}
else{
?>
  <Response>
    <Gather action="http://phone.indyhall.org/gather.php" method="POST">
      <Say>You did not make a selection or your code is invalid. If you're a guest or visitor, please press 0. Otherwise, enter your 4 digit code now.</Say>
    </Gather>
  </Response>
<?php
}
?>