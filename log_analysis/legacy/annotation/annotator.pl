#!/usr/bin/perl
#
# Copyright (C) 2018 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#


# This script processes all files with logs and produces annotations for each 
# line as either milestone met (e.g., M1) or attempted (e.g., A1) or 
# unrelated (U)
# Supply folder with output of analyze.py, text file w milestones, 
# and folder for output [optional -d for debugging]
# e.g., annotator.pl hw1-csv milestones-intro hw1-annotated

# User structure
our %users = ();
our %uc = ();

sub processline
{
    $line = shift;
    if ($line eq "")
    {
	return;
    }
    #CMBEGIN,node,time,dir,input,output,user@server
    @items = split /,/, $line;
    $us = $items[$#items];
    @elems = split /\@/, $us;
    $uid = $elems[0];
    $node = $items[1];
    $time = $items[2];
    $i = 4;
    if ($items[$i] =~ /^%/)
    {
	$input = $items[$i];
	$input =~ s/^%//;
	while ($items[$i] !~ /%$/)
	{
	    $i++;
	    $input .= $items[$i];
	}
	$input =~ s/%$//;
    }
    else
    {
	$input = $items[$i];
    }
    $i++;
    if ($items[$i] =~ /^%/)
    {
	$output = $items[$i];
	$output =~ s/^%//;
	while ($items[$i] !~ /%$/)
	{
	    $i++;
	    $output .= $items[$i];

	}
	$output =~ s/%$//;
    }
    else
    {
	$output = $items[$i];
    }
    if (!exists($users{$uid}))
    {
	$uc{$uid} = 1;
    }
    $i = $uc{$uid};
    $users{$uid}{$i}{'time'} = $time;
    $users{$uid}{$i}{'node'} = $node;
    $users{$uid}{$i}{'input'} = $input;
    $users{$uid}{$i}{'output'} = $output;
    $uc{$uid}++;
}

$usage="$0 folder-w-clean-logs file-w-milestones output-folder [-d]\n";
if ($#ARGV < 2)
{
    print $usage;
    exit(0);
}
opendir(my $dh, $ARGV[0]) || die "Can't open $ARGV[0] $!";
@files = sort (readdir $dh);

# Load user files
# do this in two passes since
# we may not be able to match
# uid in a single pass
%usermap = ();
%filemap = ();
$debug = 0;
if ($#ARGV == 3 && $ARGV[3] eq "-d")
{
    $debug = 1;
}    

for $f (@files)
{
    print "Reading $f\n";
    $fh = new IO::File($ARGV[0] . "/" . $f);
    $line = "";
    while(<$fh>)
    {
	# read a line and figure out if it is complete
	if($_ =~ /^CMBEGIN/)
	{
	    processline($line);
	    $line = $_;
	}
	else
	{
	    $line = $line . $_;
	}
    }
    processline($line);
}

# Load milestones
%milestones = ();
$fh = new IO::File($ARGV[1]);
$j = 0;
# Figure out label as last string of filename after dash
$ARGV[1] =~ /(.*)milestones-(.*)$/;
$label=$2;
while(<$fh>)
{
    @items = split /\,/, $_;
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

# Go through users and for each line figure out if a milestone was met
# or attempted, or the line is unrelated to any milestone
for $uid (keys %users)
{
    %isroot = ();
    $mintime = 0;
    $maxtime = 0;
    for $i (sort keys %{$users{$uid}})
    {
	# Remember minimum and maximum time 
	if ($users{$uid}{$i}{'time'} != 0)
	{
	    if ($mintime == 0 || $users{$uid}{$i}{'time'} < $mintime)
	    {
		$mintime = $users{$uid}{$i}{'time'};
	    }
	    if ($maxtime == 0 || $users{$uid}{$i}{'time'} > $maxtime)
	    {
		$maxtime = $users{$uid}{$i}{'time'};
	    }
	}
	
	$nummatched = 0;
	if ($debug)
	{
	    print "-------------------------------------------\n";
	    print "INPUT $uid " . $users{$uid}{$i}{'node'} . "  " . $users{$uid}{$i}{'input'} . "\n";
	}

	# Strip sudo from command and just check for denied in output
	# in the milestones
	$users{$uid}{$i}{'input'} =~ s/^sudo\s+//;

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
		$dir = "input";
		if ($pattern eq "opattern")
		{
		    $dir = "output";
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
				print "$uid: Trying to match milestone $j option $m pattern *$e* with $users{$uid}{$i}{$dir} dir $dir\n";
			    }
			    if ($users{$uid}{$i}{$dir} =~ /$e/)
			    {
				$match++;
				$matched += length $e;
			    }
			}
			# Remember how much we matched this milestone
			if ($matched > $matches{$j} && $dir eq "input")
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
			    if ($milestones{$j}{'node'} eq $users{$uid}{$i}{'node'} || $milestones{$j}{'node'} eq "*")
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
		    if ($milestones{$j}{'node'} eq $users{$uid}{$i}{'node'} || $milestones{$j}{'node'} eq "*")
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
		push(@{$users{$uid}{$i}{'milestones'}}, $j);
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
		    @el1 = split /\s+/, $users{$uid}{$i}{'input'};
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
			@el1 = split /\s+/, $users{$uid}{$i}{'input'};
			for $m (keys %{$milestones{$j}{'ipattern'}})
			{
			    @el2 = split /\s+/, $milestones{$j}{'ipattern'}{$m};
			    if ($el1[0] eq $el2[0] && $matches{$j} == $foundmatch)
			    {
				if ($debug)
				{
				    print "A: This is attempt for milestone $j\n";				
				}
				push(@{$users{$uid}{$i}{'attempts'}}, $j);
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
			    push(@{$users{$uid}{$i}{'attempts'}}, $j);
			}
		    }
		}
	    }
	}
    }
    if (!exists($users{$uid}{'mintime'}) || $users{$uid}{'mintime'} > $mintime)
    {
	$users{$uid}{'mintime'} = $mintime;
    }
    if (!exists($users{$uid}{'maxtime'}) || $users{$uid}{'maxtime'} < $maxtime)
    {
	$users{$uid}{'maxtime'} = $maxtime;
    }
}
# Print final stats
# each in their own file
# in the output folder
for $uid (sort keys %users)
{
    $filename = $ARGV[2] . "/" . $uid . "." . $label;
    print "Write to file $filename\n";
    open(my $fh, '>', $filename);
    print $fh "User $uid start time " . $users{$uid}{'mintime'} . " end " . $users{$uid}{'maxtime'} . "\n";
    print $fh "#INPUT|uniqueID|class|time|uid|node:input|output (trunc)\n";
    $cnt = 0;
    for $i (sort {$a <=> $b} keys %{$users{$uid}})
    {
	$line = "|";
	if ($users{$uid}{$i}{'time'} == 0)
	{
	    $line .= "000000000|";
	}
	else
	{
	    $line .= $users{$uid}{$i}{'time'} . "|";
	}
        $line .= "$uid|" . $users{$uid}{$i}{'node'} . ":" . $users{$uid}{$i}{'input'};
	if (scalar(@{$users{$uid}{$i}{'milestones'}}) > 0)
	{
	    for $m (@{$users{$uid}{$i}{'milestones'}})
	    {
		$line = "M$m " . $line;
	    }
	}
	elsif(scalar(@{$users{$uid}{$i}{'attempts'}}) > 0)
	{
	    for	$a (@{$users{$uid}{$i}{'attempts'}})
            {
                $line = "A$a " . $line;
            }
	}
	else
	{
	    $line = "U " . $line;
	}
	$out = substr($users{$uid}{$i}{'output'}, 0, 1000);
	$out =~ s/<NL>/\n/g;
	$out =~ s/<HT>/ /g;
	$line .= "|" . $out;
	$id = $uid . "-" . $label . "-" . $cnt;
	$cnt++;
	print $fh "INPUT|$id|$line\n";
    }
    close($fh);
}
