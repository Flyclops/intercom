<?php
header("content-type: text/xml");
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
?>

<Response>
  <Gather action="http://phone.indyhall.org/gather.php" method="POST">
    <Play>http://phone.indyhall.org/voice/Welcome4.mp3</Play>
    <Play>http://phone.indyhall.org/voice/Guest4.mp3</Play>
  </Gather>
</Response>