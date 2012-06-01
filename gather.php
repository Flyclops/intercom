<?php

require_once "couch/couch.php";
require_once "couch/couchClient.php";
require_once "couch/couchDocument.php";

require "settings.php";

$member_db = new couchClient($MEMBER_DB_HOST, $MEMBER_DB_NAME);

/*
 * get_member_by_code
 * ------------------
 * Get an array representing the member from storage.  Return null if no member
 * with the given code could be found.
 */
function get_member_by_code($code) {
  global $member_db;
  try {
	  return $member_db->getDoc($code);
  } catch ( Exception $e ) {
	  if ( $e->getCode() == 404 ) {
	    return null;
    } else {
	    die("Unable to get ".$code." : ".$e->getMessage());
    }
  }
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

function change_member_code($member, $new_code) {
  if (get_member_by_code($new_code) != null) {
    return $DUPLICATE_CODE_ERROR;
  } 
  
  $member->set( array(
    "_id" => $new_code,
    "code" => $new_code
  ) );
  
  return $SUCCESSFUL_CODE_CHANGE;
}


/*
 * get_member_tone
 * ---------------
 * Get the tone from the given member array, or fall back to some default.
 */
function get_member_tone($member) {
  if (isset($member->tone)) {
    return $member->tone;
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

#respond();
#die;

?>
