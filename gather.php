<?php

// NOTE: This is a temporary member 
//       datastore, until this is 
//       hooked up to a database.
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


/*
 * get_member_by_code
 * ------------------
 * Get an array representing the member from storage.  Return null if no member
 * with the given code could be found.
 */
function get_member_by_code($code) {
  // TODO: This should check the DB 
  //       instead of the above array.
  global $members;
  if (array_key_exists($code, $members)) {
    $member = $members[$code];
    return $member;
  }
  
  return null;
}


/*
 * change_member_code
 * ------------------
 * Change a member's code from one value to another.  Return status values for
 * if no member identified by the old code exists, or if the new code conflicts
 * with some other member's.
 */
$SUCCESSFUL_CODE_CHANGE = 0;
$DUPLICATE_CODE_ERROR = 1;
$NON_EXISTENT_MEMBER_ERROR = 2;

function change_member_code($old_code, $new_code) {
  if (get_member_by_code($old_code) == null) {
    return $NON_EXISTENT_MEMBER_ERROR;
  } elseif (get_member_by_code($new_code) != null) {
    return $DUPLICATE_CODE_ERROR;
  } 
  
  // TODO: This should just reassign
  //       the 'code' field on the 
  //       member's DB record.
  global $members;
  $members[$new_code] = $members[old_code];
  unset($members[$old_code]);
  
  return $SUCCESSFUL_CODE_CHANGE;
}


/*
 * get_member_tone
 * ---------------
 * Get the tone from the given member array, or fall back to some default.
 */
function get_member_tone($member) {
  if (array_key_exists('tone', $member)) {
    return $member['tone'];
  }
  
  return "http://idisk.s3.amazonaws.com/tmp/9.wav";
}


/*
 * ------------------------------------
 * Respond to the user input.
 */
function respond() {
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
  }
  
  elseif ($digits == '0') {
    ?>
    <Response>
      <Play>http://phone.indyhall.org/voice/FrontDesk1.mp3</Play>
      <Dial>267-702-4865</Dial>
    </Response>
    <?php
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
}

respond();
die;

?>
