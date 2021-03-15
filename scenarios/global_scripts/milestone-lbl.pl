# Continuously read csv file for this node (current only)
# and process it to annotate lines, save output locally
use IO::Handle;

# User structure

sub processline
{
    my $row = shift;
    #CMBEGIN,node,time,dir,input,output,user@server

    if (length($row) == 0) {
    	return;
    }
    my $ann_node = $row->[1];
	my $ann_time = $row->[2];
	my $ann_cwd = $row->[3];
	my $ann_input = $row->[4];
	my $ann_output = $row->[5];
	my $ann_user_prompt = $row->[6];
    my @elems = split /\@/, $ann_user_prompt;
    my $ann_uid = $elems[0];
    # print "\nNode:$ann_node,time:$ann_time,input:$ann_input,output:$ann_output,uid:$ann_uid\n";
    annotate_print($ann_time, $ann_node, $ann_input, $ann_output, $ann_uid, $ann_cwd);
}

sub annotate_print
{
	$ann_time = $_[0];
	$ann_node = $_[1];
	$ann_input = $_[2];
	$ann_output = "%" . $_[3] . "%";
	$ann_uid = $_[4];
	$ann_cwd = $_[5];

	# Initialize a counter variable to 0
	# Counter is only initialized at the time of first call to annotate_print function
	# Write structure of output file, when the annotate_print function is called for the first time
	if (!defined ($ann_counter)) {
		$ann_counter = 0;
		$filename = $ARGV[2];
		open(my $fh, '>>', $filename);
		print $fh "#INPUT|uniqueID|class|time|uid|cwd|node:input|output (trunc)\n";
		close($fh);

	}
	else {
		$ann_counter += 1;
	}

	@ann_milestones = ();
	@ann_attempts = ();
	# Go through a line and figure out if a milestone was met
	# or attempted, or the line is unrelated to any milestone
	$nummatched = 0;
	if ($debug)
	{
	    print "-------------------------------------------\n";
	    print "INPUT $ann_uid " . $ann_node . "  " . $ann_input . "\n";
	}

	# Strip sudo from command and just check for denied in output
	# in the milestones
	$ann_input =~ s/^sudo\s+//;

	# We will use this to remember how well
	# we matched each milestone so we can
	# identify attempts
	%matches = ();
	for $m (keys %milestones)
	{
	    $matches{$m} = 0;
	}
	# Try to match each milestone
	for $j (sort keys %milestones)
	{
	    if ($debug)
	    {
		print "MILESTONE $j\n";
	    }
	    $matchedinput = 0;
	    $matchedoutput = 0;

	    # Check for pattern
	    for $pattern ("ipattern", "opattern")
	    {
		$dir = "ann_input";
		if ($pattern eq "opattern")
		{
		    $dir = "ann_output";
		}
		if ($milestones{$j}{$pattern}{0} ne "*")
		{
		    $tmatch = 0;
		    # Try to match each alternative in the pattern
		    for $m (keys %{$milestones{$j}{$pattern}})
		    {
			$k = $milestones{$j}{$pattern}{$m};
			@elems = split /\s+/, $k;
			$match = 0;
			$matched = 0;

			# Try to match each word separately
			for $e (@elems)
			{
			    if ($debug)
			    {
				print "$ann_uid: Trying to match milestone $j option $m pattern *$e* with ${$dir} dir $dir\n";
			    }
			    if (${$dir} =~ /$e/)
			    {
				$match++;
				$matched += length $e;
			    }
			}
			# Remember how much we matched this milestone
			if ($matched > $matches{$j} && $dir eq "ann_input")
			{
			    $matches{$j} = $matched;
			    if ($debug)
			    {
				print "Matched $matches{$j} characters\n";
			    }
			}
			# If we matched all the words, we matched the pattern
			if ($match == scalar(@elems))
			{
			    # But only if we're on the right node
			    if ($milestones{$j}{'node'} eq $ann_node || $milestones{$j}{'node'} eq "*")
			    {
				if ($pattern eq "ipattern")
				{
				    $matchedinput = 1;
				}
				else
				{
				    $matchedoutput = 1;
				}

				if ($debug)
				{
				    print "\t\tMatched $dir for milestone $j!\n";
				}
			    }
			}
		    }
		}
		else
		{
		    # But only if we're on the right node
		    if ($milestones{$j}{'node'} eq $ann_node || $milestones{$j}{'node'} eq "*")
		    {
			# Matched star input/output
			if ($pattern eq "ipattern")
			{
			    $matchedinput = 1;
			}
			else
			{
			    $matchedoutput = 1;
			}
		    }
		}
	    }

	    # Check if both input and output matched, if so this milestone
	    # was matched
	    if ($matchedinput == 1 && $matchedoutput == 1)
	    {
		if ($debug)
		{
		    print "\t\t Fully matched milestone $j\n";
		}
		push(@ann_milestones, $j);
		$nummatched++;
	    }
	}
	# No milestone was matched, see if we can identify what was attempted
	if ($nummatched == 0)
	{
	    # Find max match
	    $max = 0;
	    for $j (keys %matches)
	    {
		if ($matches{$j} > $max)
		{
		    $max=$matches{$j};
		}
	    }
	    if ($max > 0)
	    {
		# Multiple milestones could have been attempted
		# give preference to those that use the same command
		# as input
		$foundmatch = 0;
		for $j (keys %matches)
		{
		    @el1 = split /\s+/, $ann_input;
		    for $m (keys %{$milestones{$j}{'ipattern'}})
		    {
			@el2 = split /\s+/, $milestones{$j}{'ipattern'}{$m};
			if ($el1[0] eq $el2[0] && $matches{$j} > $foundmatch)
			{
			    if ($debug)
			    {
				print "A: This could be attempt for milestone $j\n";
			    }
			    $foundmatch = $matches{$j};
			}
		    }
		}
		if ($foundmatch > 0)
		{
		    for $j (keys %matches)
		    {
			@el1 = split /\s+/, $ann_input;
			for $m (keys %{$milestones{$j}{'ipattern'}})
			{
			    @el2 = split /\s+/, $milestones{$j}{'ipattern'}{$m};
			    if ($el1[0] eq $el2[0] && $matches{$j} == $foundmatch)
			    {
				if ($debug)
				{
				    print "A: This is attempt for milestone $j\n";
				}
				push(@ann_attempts, $j);
			    }
			}
		    }
		}
		# Match wasn't found, get all the candidates as attempts
		if (!$foundmatch)
		{
		    for $j (keys %matches)
		    {
			if ($matches{$j} == $max)
			{
			    if ($debug)
			    {
				print "A: This was attempt for milestone $j\n";
			    }
			    push(@ann_attempts, $j);
			}
		    }
		}
	    # }
	}
    }

	# Print final stats
	# each in their own file
	# in the output folder
    $filename = $ARGV[2];
    # print "Write to file $filename\n";
    open(my $fh, '>>', $filename);
	$line = "|";
	if ($ann_time == 0)
	{
	    $line .= "000000000|";
	}
	else
	{
	    $line .= $ann_time . "|";
	}
        $line .= "$ann_uid|" . "$ann_cwd|" .  $ann_node . ":" . $ann_input;
	if (scalar(@ann_milestones) > 0)
	{
	    for $m (@ann_milestones)
	    {
		$line = "M$m " . $line;
	    }
	}
	elsif(scalar(@ann_attempts) > 0)
	{
	    for	$a (@ann_attempts)
            {
                $line = "A$a " . $line;
            }
	}
	else
	{
	    $line = "U " . $line;
	}
	$out = substr($ann_output, 0, 1000);
	$out =~ s/<NL>/\n/g;
	$out =~ s/<HT>/ /g;
	$line .= "|" . $out;
	$id = $ann_uid . "-" . $label . "-" . $ann_counter;
	print $fh "INPUT|$id|$line\n";
    close($fh);
}

$usage="$0 file-w-milestones csv-file-to-annotate output-file [-d]\n";
if ($#ARGV < 2)
{
	print "len is $#ARGV\n";
    print $usage;
    exit(0);
}

# Set debug flag
use Getopt::Long qw(GetOptions);
$debug;
GetOptions('-d' => \$debug);

# Load milestones
%milestones = ();
$fh = new IO::File($ARGV[0]);
$j = 0;
# Use constant label
$label="ulab";
while(<$fh>)
{
    @items = split(/\,/, $_);
    $milestones{$j}{'node'} = $items[0];
    # Load input and output milestone clues
    for ($k=1; $k<=2;$k++)
    {
	@elems = split /\|/, $items[$k];
	$pattern = "ipattern";
	if ($k == 2)
	{
	    $pattern = "opattern";
	}

	# Split if there are multiple patterns
	for ($i=0; $i <= $#elems; $i++)
	{
	    $elems[$i] =~ s/\n//g;
	    $elems[$i] =~ s/^\s+//;
	    $elems[$i] =~ s/\s+$//;
	    # Remember the pattern, each element separately
	    # so we could match for reordered args too
	    $milestones{$j}{$pattern}{$i} = $elems[$i];
	    if ($debug)
	    {
		print "Milestone $j pattern $pattern for $i is $elems[$i]\n";
	    }
	}
    }
    $j++;
}

# Text::CSV_XS module is used to parse CSV
use Text::CSV_XS;
my $input_csv_file = $ARGV[1];
open my $FH, "<:encoding(utf8)", "$input_csv_file" or die "$input_csv_file: $!";
my $csv = Text::CSV_XS->new ({ binary => 1, quote_char => "%", escape_char => "%" }) or die "Cannot use CSV: ".Text::CSV->error_diag ();

# Time::HiRes module is used to sleep for miliseconds, since native sleep fucntion only allows integers
use Time::HiRes;
# Poll the file forever
while(true)
{
 	#read file in while loop
	# csv-> getline method returns an array reference
	while (my $row = $csv->getline ($FH) ) {
		if (length($row) > 0) {
			processline($row);
		}
	}
   Time::HiRes::sleep(0.1);
   seek($fh, 0, 1);
}


