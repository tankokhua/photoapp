#!/usr/local/bin/perl
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#     Author: <wongshihnern@micron.com>
# Time-stamp: <17 Dec 2008 11:10:52 AM wongshihnern>
# Micron Semiconductor Asia Confidential and Proprietary
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Repondez S'il Vous Plait, French for "Please reply"
use warnings;
use strict;
use lib '.';
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;
use GenLib;
use Micron::WebCommon;
my $query = new CGI;

my $organizers = '^tankokhua|chankl|chuakc|siangleong|rogerhor|ggerard|derzhan|dhika$';
my $edt = '^patrickplim|takhan|wuping|linzhu|shenzm|cheongcheewa|cheeweihua|linxiuqing|haymunwin|laichiwai|sflee|jiangt|maksaifung|chankeesoon|lawtchai$';
my $idfile='/u/te_event/public_html/events/test_games_2013/cache_id.txt';
my $rsvpfile='/u/te_event/public_html/events/test_games_2013/temp/rsvp.txt';
my $currentuserprefs;
my $remotehost=remote_host().' ('.remote_addr().')';
my $userid=remote_host();
$userid=~s/\..+$//;
my $authenticateduser;
my $huserid=getphUserid($userid, $idfile);
my @supervisors=qw/thengcheng cheez sengyew allee rsumaputra lrdeguzm chankl/;
my @preferences=qw/userid attending driving dummy comments remotehost timestamp/;
my $is_supervisor=0;
foreach (@supervisors){if($userid eq $_){$is_supervisor=1;last;}}
print $query->header(-nph=>0,
		     -status=>'200 OK',
		     -expires=>'+1s',
		     -type=>'text/html');
print $query->start_html('TE Hunger Games 2013');

#unless (defined $huserid) {
 $userid=GetLoginUsername();
 $authenticateduser=$userid;
 $huserid=getphUserid($userid, $idfile);
#}


print '<link rel="stylesheet" type="text/css" href="./events.css">';
#print $query->h1("$userid, $remotehost");

while (<DATA>) {
  print;
}

`touch $rsvpfile`;
`chmod og-rw $rsvpfile`;

#Initialize boss's preferences
#foreach (@supervisors) {
#  my $lastline=linefromfile(lc($_), $rsvpfile);
#  unless (defined $lastline) {
#    $currentuserprefs->{'remotehost'}=$remotehost;
#    $currentuserprefs->{'userid'}=$_;
#    $currentuserprefs->{'timestamp'}=createDateTimeStringSafe();
#    line2file(join('|', @$currentuserprefs{@preferences}), $rsvpfile);
#  }
#}

#if (defined $huserid and -w $rsvpfile) {
if (defined $huserid ) {
  if ($query->param() and (defined $query->param('Button')) and $query->param('Button') eq 'Submit') {
   # print $query->param('Button')."-----<br>\n";
    foreach (@preferences) {
      if (defined $query->param($_)) {
	#print "$_ - ".$query->param($_)."--<br>\n";
	$currentuserprefs->{$_}=$query->param($_);
	$currentuserprefs->{$_}=~s/\|//g;
      } else {
	$currentuserprefs->{$_}='';
      }
    }
    $currentuserprefs->{'remotehost'}=$remotehost;
    $currentuserprefs->{'userid'}=$userid;
    $currentuserprefs->{'timestamp'}=createDateTimeStringSafe();
    line2file(join('|', @$currentuserprefs{@preferences}), $rsvpfile);
  } else {
    my $lastline=linefromfile($userid, $rsvpfile);
    if (defined $lastline) {
      my @lastprefs=split(/\|/, $lastline);
      my $ii=0;
      foreach (@preferences) {
	#print $preferences[$ii].' - '.$lastprefs[$ii]."\n";
	$query->param(-name=>$preferences[$ii],-values=>$lastprefs[$ii]) unless ($lastprefs[$ii] eq '');
	$currentuserprefs->{$preferences[$ii]}=$lastprefs[$ii];
	$ii++;
      }
    } else {
      $currentuserprefs->{'remotehost'}=$remotehost;
      $currentuserprefs->{'userid'}=$userid;
      $currentuserprefs->{'timestamp'}=createDateTimeStringSafe();
      line2file(join('|', @$currentuserprefs{@preferences}), $rsvpfile);
    }
  }
# print '<center><h2>RSVP</h2>';
  print '<br><h2 id="center" >Invitation to TE Hunger Games (26 Mar 2013)</h2>';
  print '<center><img src="capitol.bmp" style="padding-left:0px"></center>';
  print '<br><h1 style="text-align:center">KEEP CALM AND MAY THE ODDS BE EVER IN YOUR FAVOR</h1>';
  print start_form;
  print table({-cellpadding=>5 },
	      Tr({-class=>'formtable'},
		 [
		  td(['Name']).td(textfield(-name=>'name',
					    -size=>80,
					    -override=>1,
					    -readonly=>'readonly',
					    -disabled=>'disabled',
					    -default=>$huserid->{'name'},
					   )),
		  td(['Attending']).td(radio_group(
						   -name=>'attending',
						   -Values=>['yes','no'],
						   -labels=>{'yes'=>'Yes',
							     'no'=>'No',
							    },
						   -default=>$currentuserprefs->{'attending'}
						  ).' &nbsp;&nbsp;&nbsp;&nbsp;Please confirm by 15 Mar (Fri).'),
		  td(['Driving']).td(popup_menu(-name=>'driving',
						  -values=>[qw/no yes/],
						  -labels=>{'yes'=>'Yes',
							    'no'=>'No',
							   },
						  -default=>$currentuserprefs->{'driving'}
						 )),
		  td(['Comments']).td(textfield(-name=>'comments',
						-size=>80,
						-maxlength=>80,
						-default=>$currentuserprefs->{'comments'},
					       ).' Suggestions/Feedback, etc.'),
		 ]
		)
	     );

  print '<p>';
# unless ($is_supervisor == 1) {
#   print 'Supervisor ';
#   print $query->popup_menu(
#			     -name=>'supervisor',
#			     -Values=>[(sort @supervisors,'')],
#			     -default=>'').' (Names grouped by supervisor; leave blank if supervisor not in selection)';
#  }
  print '<p align="center">',
    submit(-name=>'Button',
           -class=>'submit',
           -value=>'Submit'),
#     defaults,
	br, br,
        '(If you encounter SiteMinder error, please open a new browser, and try again.)',
	end_form;
#if (defined $authenticateduser) {
#	print "<h3>Please close browser window to change authenticated user ($authenticateduser)</h3>";
#}
  print	  hr;
} elsif (! -w $rsvpfile) {
  print "<h3>Maintenance mode...or event over. Please check back later</h3><hr>";
} else {
  print "Sorry, your userid cannot be determined from your host. Please send mail to <a href=\"mailto:tankokhua\@micron.com?body=userid and preferences&subject=Christmas Lunch RSVP\">tankokhua\@micron.com</a> with your userid and preferences.<br>";}

# my $huserid=getphUserid($userid, $idfile);
# foreach (keys %$huserid) {
#   print $huserid->{$_}."<br>\n";
# }


open(RSVP, "< $rsvpfile");
my @rsvplist;
while (<RSVP>) {
# print "$_<br>";
  push @rsvplist, [split(/\|/)];
}
close RSVP;

print '<h2 id="center">Responses</h2>';
print '<table align="center" class="rsvptable" slColor="gold" hlColor="#8FBC8F">';
#print "<thead><tr><th>".join('</th><th>', qw/&nbsp; Name Supervisor Attending Halal Vegetarian Driving Comments\/Suggestions/, 'Last update')."</th></tr></thead>";
if ($userid =~ /$organizers/) {
  print "<thead><tr><th>".join('</th><th>', qw/&nbsp; Name Attending Driving/,                 'Comments', 'Last Update')."</th></tr></thead>";
} else {
  print "<thead><tr><th>".join('</th><th>', qw/&nbsp; Name Attending Driving/,                 'Comments', 'Last Update')."</th></tr></thead>";
}




sub replace_with_ticks{
  my $inarray=shift;
  my $ii;
  foreach (@$inarray) {
    if ($_ eq 'yes') {
      $inarray->[$ii]='<center><img src="tick.gif" width=11 height=11 align=top border=0 alt="Yes"></center>';
    } elsif ($_ eq 'no') {
      $inarray->[$ii]='&nbsp;';
      $inarray->[$ii]='<center><img src="cross.gif" width=11 height=11 align=top border=0 alt="No"></center>';
    }
    $ii++;
  }
}

my @counts;
#foreach my $curboss (@supervisors) {
  foreach (@rsvplist) {
    my @fields=@$_;
    my $huserid=getphUserid($fields[0], $idfile);
    my @columns = ();
#   next unless ($huserid->{'userid'} eq $curboss);
#   next if ($huserid->{'userid'} eq 'atcy'); #not inside invitation list
    my $empid=$huserid->{'empid'};
    my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">$empid</a>";
    my $emailid=$huserid->{'userid'};
    my $emaillink="<a href=\"mailto:$emailid\@micron.com\">".$huserid->{'name'}."</a>";
   #my @columns=($emplink, $emaillink, @$_[1..4,6]);
    if ($userid =~ /$organizers/) {
      @columns=($emplink, $emaillink, @$_[1,2,4,6]);
    } else {
      @columns=($emplink, $emaillink, @$_[1,2,4,6]);
    }
    replace_with_ticks(\@columns);
    for my $ii (1..$#columns) {
      if ($columns[$ii]=~/yes/i) {
	$counts[$ii]++;
      }
    }
    next if (($fields[0]=~ /$organizers/) && ($userid !~ /$organizers/));
    print '<tr class="bossrow"><td NOWRAP>';
    print join('</td><td NOWRAP>', @columns);
    print '</td></tr>';
  }
# foreach (@rsvplist) {
#   my @fields=@$_;
#   next unless ($fields[1] eq $curboss);

#   print '<tr><td NOWRAP>';
#   my $huserid=getphUserid($fields[0], $idfile);
#   my $empid=$huserid->{'empid'};
#   my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">$empid</a>";
#   my $emailid=$huserid->{'userid'};
#   my $emaillink="<a href=\"mailto:$emailid\@micron.com\">".$huserid->{'name'}."</a>";
#  #my @columns=($emplink, $emaillink, @$_[1..4,6]);
#   my @columns=($emplink, $emaillink, @$_[1,2,3,5]);
#   replace_with_ticks(\@columns);
#   print join('</td><td NOWRAP>', @columns);
#   for my $ii (1..$#columns) {
#     if ($columns[$ii]=~/yes/i) {
#$counts[$ii]++;
#     }
#   }
#   print '</td></tr>';
# }
#}

#Print all those without a valid supervisor
 if (1==2) {
  foreach (@rsvplist) {
   my @fields=@$_;
   my $isorphan=1;
   foreach my $boss (@supervisors) {
     if ($fields[1] eq $boss or $fields[0] eq $boss) {
       $isorphan=0;
       last;
     }
   }
   next unless ($isorphan==1);
 
   print '<tr class="orphanrow"><td NOWRAP>';
   my $huserid=getphUserid($fields[0], $idfile);
   my $empid=$huserid->{'empid'};
   my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">$empid</a>";
   my $emailid=$huserid->{'userid'};
   my $emaillink="<a href=\"mailto:$emailid\@micron.com\">".$huserid->{'name'}."</a>";
   my @columns=($emplink, $emaillink, @$_[1..4,6]);
   replace_with_ticks(\@columns);
   print join('</td><td NOWRAP>', @columns);
   for my $ii (1..$#columns) {
     if ($columns[$ii]=~/yes/i) {
       $counts[$ii]++;
     }
   }
   print '</td></tr>';
  }
 }

if ($userid =~ /$organizers/ ) {
 print '<tfoot><tr><td NOWRAP>';
 print join('</td><td NOWRAP>', @counts);
 print '</td></tr></tfoot>';
}
print '</table><br>';
if($userid =~ /$organizers/ ) {
print 'Total number of responses: '.scalar(@rsvplist).'<br><br>';
}
print '</center>';

#} # organiser check
##############
# print '<table>';
# foreach (@supervisors) {
#   print '<tr><td NOWRAP>';
#   my $userid=lc($_);
#   my $huserid=getphUserid($userid, $idfile);
#   print join('</td><td NOWRAP>',values %$huserid);
#   print '</td></tr>';
# }
# print '</table>';
#if(1==2) {
if ($userid =~ /$organizers/) {
 my %responded;
 my $numinvite=0;
 my $subtotal = 0;
 my $namelist = "";
 print '<hr><div style="width:800px">';
 print "<h4>For organizers only</h4>";

 map { if ($_->[1] eq 'yes') { $namelist .= $_->[0].'; '; $subtotal++; }
     $responded{$_->[0]}++;
 } @rsvplist;
 print "<br><b>Attending ($subtotal)</b><br>";
 print "$namelist";
 $subtotal = 0; $namelist = "";

 map { if ($_->[2] eq 'yes') { $namelist .= $_->[0].'; '; $subtotal++; } } @rsvplist;
 print "<br><br><b>Driving ($subtotal)</b><br>";
 print "$namelist";
 $subtotal = 0; $namelist = "";

 map { if ($_->[1] eq 'no') { $namelist .= $_->[0].'; '; $subtotal++; } } @rsvplist;
 print "<br><br><b>Not Attending ($subtotal)</b><br>";
 print "$namelist";
 $subtotal = 0; $namelist = "";

 map { 
       if ($_->[1] ne 'no' and $_->[1] ne 'yes' and $_->[0]!~/$edt/) 
       { 
	 $namelist .= $_->[0].'; '; $subtotal++; } 
       elsif ($_->[1] ne 'no' and $_->[1] ne 'yes' and $_->[0]=~/$edt/) 
       {
         $namelist .= '<b>'.$_->[0].'</b>; '; $subtotal++;  
       }
 } @rsvplist;
 print "<br><br><b>Undecided ($subtotal)</b><br>";
 print "$namelist";
 $subtotal = 0; $namelist = "";

 map { 
	if (!exists($responded{$_}))
	{
           if($_!~/$edt/) {
             $namelist .= "$_; ";
           } else {
             $namelist .= "<b>$_</b>; ";
           }
	   $subtotal++;
	}
		#$namelist .= "$_; " unless $responded{$_};
        $responded{$_}=99;
        $numinvite++;
 } split(/;\s*/, 'aemorada; ahsia; allee; anqin; bcchiam; boonping; boonzhiu; cgarcia; chankeesoon; chankl; cheehau; cheekheng; cheeweihua; cheez; chengwp; cheongcheewa; chewkorkiat; chinhoi; choonhian; christinelis; chuahweehoon; chuakc; chuaszemin; cjlim; ckuah; cranchores; derzhan; dhika; dpgallo; dprotoma; empeleo; enghai; ggerard; gng; gordonchin; hanjian; hanny; haymunwin; howboonseng; huaiseng; huifen; huikhim; humengsa; hychong; imkeh; irfanabid; irisyong; jamestacata; jdomingo; jglim; jiangt; jlgaray; jocelynkang; johnkohwtze; joycetuge; jrmalics; jtbaclig; junnan; jvalient; kcheng; kienhan; kiewjs; klee; kongmin; laichiwai; laukokcheng; lawtchai; leeweibing; leongkk; leongkw; limkl; linxiuqing; linzhu; lonepyae; loyteckpui; lrdeguzm; maksaifung; markanthony; marychay; mchin; mohdsarni; ngcw; norefel; nyetyun; patrickplim; pgdelac; pohhong; rafael; rbmacabi; rogerhor; rsumaputra; schai; scydesmond; sengyew; sflee; shenzm; sherynseah; siangleong; siauckean; simonlai; skurniawan; stanleylai; stvong; suklee; sunshu; surang; syapyap; takhan; tanchiayng; tankkiang; tankokhua; tanszeluan; teheexyan; thengcheng; thyeo; tongxue; vguillermo; vijayakumar; wailynn; weekiat; wongshihnern; wuping; yeewan; ysgoh; zhanghong; zwee; ehgan');
 print "<br><br><b>Not visited site yet ($subtotal)</b><br>";
 print "$namelist";

 print "</div><br><br>";
}

if (1==2) {
#if ($userid eq 'tankokhua') {
   my %responded;
   my $numinvite=0;
   print '<h3>Current Distribution list (Visited Site)</h3>';
   map { my $huserid=getphUserid($_->[0], $idfile);
        my $empid=$huserid->{'empid'};
        my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">".$_->[0]."; </a>";
        print "$emplink";
       #print "$emplink" unless ($huserid->{'userid'} eq 'atcy'); #not inside invitation list
        $responded{$_->[0]}++;
   } @rsvplist;
   print '<h3>Current Distribution list (Attending)</h3>';
   map { if ($_->[2] eq 'yes') { print $_->[0].'; '; } } @rsvplist;
   print '<h3>Current Distribution list (Undecided)</h3>';
   map { if ($_->[2] ne 'no' and $_->[2] ne 'yes') { print $_->[0].'; '; } } @rsvplist;
   print '<h3>Current Distribution list (Driving)</h3>';
   map { if ($_->[3] eq 'yes') { print $_->[0].'; '; } } @rsvplist;
   print '<h3>Current Distribution list (Not visited site yet)</h3>';
   map { my $huserid=getphUserid($_, $idfile);
        my $empid=$huserid->{'empid'};
        my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">$_; </a>";
        print "$emplink" unless $responded{$_};
        $responded{$_}=99;
        $numinvite++;
   } split(/;\s*/, 'aemorada; ahsia; allee; anqin; bcchiam; boonping; boonzhiu; cgarcia; chankeesoon; chankl; cheehau; cheekheng; cheeweihua; cheez; chengwp; cheongcheewa; chewkorkiat; chinhoi; choonhian; christinelis; chuahweehoon; chuakc; chuaszemin; cjlim; ckuah; cranchores; derzhan; dhika; dpgallo; dprotoma; empeleo; enghai; ggerard; gng; gordonchin; hanjian; hanny; haymunwin; howboonseng; huaiseng; huifen; huikhim; humengsa; hychong; imkeh; irfanabid; irisyong; jamestacata; jdomingo; jglim; jiangt; jlgaray; jocelynkang; johnkohwtze; joycetuge; jrmalics; jtbaclig; junnan; jvalient; kcheng; kienhan; kiewjs; klee; kongmin; laichiwai; laukokcheng; lawtchai; leeweibing; leongkk; leongkw; limkl; linxiuqing; linzhu; lonepyae; loyteckpui; lrdeguzm; maksaifung; markanthony; marychay; mchin; mohdsarni; ngcw; norefel; nyetyun; patrickplim; pgdelac; pohhong; rafael; rbmacabi; rogerhor; rsumaputra; schai; scydesmond; sengyew; sflee; shenzm; sherynseah; siangleong; siauckean; simonlai; skurniawan; stanleylai; stvong; suklee; sunshu; surang; syapyap; takhan; tanchiayng; tankkiang; tankokhua; tanszeluan; teheexyan; thengcheng; thyeo; tongxue; vguillermo; vijayakumar; wailynn; weekiat; wongshihnern; wuping; yeewan; ysgoh; zhanghong; zwee; ehgan');
  
   print "<p>Invited: $numinvite</p>";
  
   foreach my $uid (keys %responded) {
    if ($responded{$uid}!=99) {
      my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$uid\">$uid; </a>";
      print "$emplink<br>\n";
    }
   }
}

#if ($userid eq 'tankokhua') {
if (1==2) {
   print '<h2>Responses</h2>';
   print '<table align="center" class="rsvptable" slColor="gold" hlColor="#8FBC8F">';
###print "<thead><tr><th>".join('</th><th>', qw/&nbsp; Name Supervisor Attending Halal Vegetarian BusTransport Comments\/Suggestions/, 'Last update')."</th></tr></thead>";
   print "<thead><tr><th>".join('</th><th>', qw/&nbsp; Name Attending BusTransport Comments/, 'Last update')."</th></tr></thead>";
  
   @counts=();
   foreach (@rsvplist) {
    my @fields=@$_;
    my $huserid=getphUserid($fields[0], $idfile);
    my $empid=$huserid->{'empid'};
    my $emplink="<a href=\"http://iisprod.micron.com/emp/default.asp?emp=$empid\">$empid</a>";
    my $emailid=$huserid->{'userid'};
    my $emaillink="<a href=\"mailto:$emailid\@micron.com\">".$huserid->{'name'}."</a>";
    my @columns=($emplink, $emaillink, @$_[1..4,6]);
    next unless ($columns[4] eq 'yes');
    replace_with_ticks(\@columns);
    print '<tr><td NOWRAP>';
    print join('</td><td NOWRAP>', @columns);
    for my $ii (1..$#columns) {
      if ($columns[$ii]=~/yes/i) {
        $counts[$ii]++;
      }
    }
    print '</td></tr>';
   }
  
   print '<tfoot><tr><td NOWRAP>';
   print join('</td><td NOWRAP>', @counts);
   print '</td></tr></tfoot>';
   print '</table>';
}


print <<'ENDHTML';

ENDHTML






print end_html;





__DATA__
<link REL="StyleSheet" HREF="http://merc.micron.com/stylesheet/merc_style.css" TYPE="text/css" MEDIA="screen" />

<!--- ***************************************** --->
<!--- BEGIN JAVASCRIPT FOR DROP DOWN MENUS	--->
<!--- ***************************************** --->
<script language="JavaScript1.2">
	var isLoaded = 0;
	var isMenu = 0;
	var isFrames = 0;
	var stat = "Welcome";
</script>
<script LANGUAGE="JavaScript1.2" SRC="http://merc.micron.com/menus/HM_Loader.js" TYPE="text/javascript"></script>
<!--- REPLACE @ with the path down from the web server root --->
<SCRIPT LANGUAGE='JavaScript1.2' SRC='/~wongshih/event1/menus/ex_HM_Arrays_MicronBlue.js' TYPE='text/javascript'></SCRIPT>
<SCRIPT LANGUAGE='JavaScript1.2' SRC='/~wongshih/event1/menus/ex_HM_Arrays_MicronGreen.js' TYPE='text/javascript'></SCRIPT>
<script language="JavaScript">
<!---
	document.write("<SCR" + "IPT LANGUAGE='JavaScript1.2' SRC='http://merc.micron.com/menus/HM_Script"+ HM_BrowserString +".js' TYPE='text/javascript'></SCR" + "IPT>");
//--->
</script>
<!--- ***************************************** --->
<!--- END JAVASCRIPT FOR DROP DOWN MENUS	--->
<!--- ***************************************** --->


<body leftmargin="0" rightmargin="0" bottommargin="0" topmargin="0" marginheight="0" marginwidth="0" bgcolor=white>

<!--- ***************************************** --->
<!--- TOP NAVIGATION BEGINS HERE		--->
<!--- ***************************************** --->
<TABLE border="0" cellspacing="0" cellpadding="0">
<tr>
	<td rowspan="2" valign="middle" align="left"><a href="/~te_event/" style="font-weight: bold; text-decoration: none;">Home</a></td>
	<td width="30" align="right"><img src="http://imgprod.micron.com/corp/merc/1-1.gif" hspace="0" align="right" width="50" height="24" border="0"></td>
	<td background="http://imgprod.micron.com/corp/merc/1-2.gif">&nbsp;</td>
	<td background="http://imgprod.micron.com/corp/merc/1-4.gif" width="55"><img src="http://imgprod.micron.com/corp/merc/1-3.gif" width="55" height="24" border="0" alt=""></td>
	<td background="http://imgprod.micron.com/corp/merc/1-4.gif" align="right" class="topnav" width="100%">
<!--- ***************************************** --->
<!--- BLUE NAV BEGINS HERE			--->
<!--- ***************************************** --->
		<a href="http://merc.micron.com" class="nav">MERC</a> |
		<a href="http://webservices.micron.com/" class="nav">Corporate Web Services</a> |
		<a href="http://htmlprod.micron.com/webapps/adm/corporate_affairs/caindex.htm" class="nav">Corporate Affairs</a><font color="#ffffff"> |
		<a href="http://htmlprod.micron.com/webapps/is/cmpsrv/isdoc/index.shtml" class="nav">ISDoc</a> |
		<a href="http://htmlprod.micron.com/webapps/is/cmpsrv/sst/sstportal/" class="nav">SST</a>
<!--- ***************************************** --->
<!--- BLUE NAV ENDS HERE			--->
<!--- ***************************************** --->
	</td>
	<td rowspan="3"><a href="http://merc.micron.com"><img src="http://imgprod.micron.com/corp/merc/logo2.gif"  border="0"></a></td>
</tr>
<tr>
	<td width="30" align="right">
		<img src="http://imgprod.micron.com/corp/merc/2-1.gif" hspace="0" align="right" width="50" height="28" border="0" alt="">
	</td>
	<td background="http://imgprod.micron.com/corp/merc/2-2.gif" colspan="2">&nbsp;</td>
	<td background="http://imgprod.micron.com/corp/merc/2-2.gif">&nbsp;</td>
</tr>


<tr>
	<td width="114" align="right"><img src="http://imgprod.micron.com/corp/merc/3-1.gif" width="114" height="23" border="0" alt=""></td>
	<td width="100%" colspan="4" align="right" background="http://imgprod.micron.com/corp/merc/3-2.gif" class="botnav">
<!--- ***************************************** --->
<!--- Green Nav Starts Here						--->
<!--- ***************************************** --->
<!---
	<a href="javascript:void(0)" class="nav" onMouseOver="popUp('elMenu1',event)" onMouseOut="popDown('elMenu1')" onClick="return false">drop down 1</a> |
	<a href="javascript:void(0)" class="nav" onMouseOver="popUp('elMenu2',event)" onMouseOut="popDown('elMenu2')" onClick="return false">drop down 2</a> |
	<a href="javascript:void(0)" class="nav" onMouseOver="popUp('elMenu3',event)" onMouseOut="popDown('elMenu3')" onClick="return false">drop down 3</a>
 --->
<!--- ***************************************** --->
<!--- Green Nav Ends Here						--->
<!--- ***************************************** --->
	</td>
</tr>
</TABLE>
<!--- ***************************************** --->
<!--- TOP NAVIGATION ENDS HERE					--->
<!--- ***************************************** --->


<TABLE border="0" cellpadding="0" cellspacing="0">
<tr>
	<td valign="top" width="160">
<!--- ***************************************** --->
<!--- GREY NAV STARTS HERE			--->
<!--- ***************************************** --->
		<TABLE bgcolor="#ffffff" border="0" cellspacing="0" cellpadding="0" width="160">
		<tr>
			<td  valign="top" style="padding-bottom: 10px">
				<a href="/"><b>Test Engineering</b></a>
			</td>
		</tr>
		<tr>
                    <td valign="top"><b>TE Team Building 2013</b>
                        <img src="hg.jpg" style="padding:5px">
		    </td>
		</tr>
		</TABLE>
<!--- ***************************************** --->
<!--- GREY NAV ENDS HERE						--->
<!--- ***************************************** --->
</td>
<td valign="top">

<!--- ***************************************** --->
<!--- ************** BEGIN CONTENT ************ --->
<!--- ***************************************** --->
