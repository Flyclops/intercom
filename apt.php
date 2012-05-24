<?php
header("content-type: text/xml");
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>

<Response>
  <Gather action="http://phone.indyhall.org/gather.php" method="POST">
    <Say>If you're a guest or visitor, please press 0. Otherwise, enter your 4 digit code now.</Say>
  </Gather>
</Response>