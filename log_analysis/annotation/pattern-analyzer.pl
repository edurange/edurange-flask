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

# Takes one file with attempts or unrelated lines, and another with milestones
# Groups lines by node, command, args, etc. for easier analysis
# some lines could be ignored if necessary
# Works best on the output of preprocess-unique.pl because it only analyzes
# unique lines

# Produces two .gv files, which can be converted to ps by doing
# dot -Tps filename.gv -o filename.ps
# See https://www.graphviz.org/pdf/dotguide.pdf


# To control the size of output adjust SMALL parameter
# Values are between 0 and 1 with smaller values giving
# larger output. Print only commands/arguments that contribute
# to higher fraction of all lines than SMALL
$SMALL = 0.05;

sub escape
{
    $string = shift;
    $string =~ s/\\/\\\\/g;
    $string =~ s/\"/\\\"/g;
    return $string;
}

$usage="$0 file-to-analyze file-w-milestones\n";
if ($#ARGV < 1)
{
    print $usage;
    exit(0);
}
%ncs = ();
%cmds = ();
%addedcmds = ();
%nodecmds = ();
%cmduse=();
%printedcmds=();
$all = 0;

# Read candidate commands from milestone file
$fh = new IO::File($ARGV[1]);
while(<$fh>)
{
    @items = split /\,/, $_;
    @elems = split /\|/, $items[1];
    for $e (@elems)
    {
	$e =~ s/sudo //;
	@words  = split /\s+/, $e;
	$addedcmds{$words[0]} = 1;
    }
}
close($fh);
$fh = new IO::File($ARGV[0]);
while(<$fh>)
{
    $line = $_;
    $i = index $_, '>';
    if ($i > -1)
    {
	$line = substr $line, 0, $i-1;
    }
    @items = split /\s+/, $line;

    $cmd = $items[1];
    @elems = split(/\:/, $cmd);
    $maincmd = $elems[1];
    $node = $elems[0];
    $nodecmds{$node} = 0;
    # is it misspelled?
    $found = 0;

    if (exists($addedcmds{$maincmd}))
    {
	$found = 1;
    }
    else
    {
	open(WHICH, "which $maincmd|" );
	while(<WHICH>)
	{
	    $found = 1;
	}
    }
    if (!$found && $maincmd ne "cd")
    {
	$cmd = "$node:misspelled";
	$maincmd = "misspelled";
    }
    
    $ncs{$cmd} += $items[0];
    $all += $items[0];
    if ($maincmd eq "misspelled")
    {
	next;
    }

    $options = "";
    $cmduse{$maincmd}{'cnt'} += $items[0];
    for ($i = 2; $i <= $#items; $i++)
    {
	if ($items[$i] =~ /^\-/)
	{
	    if (index($options, $items[$i]) == -1)
	    {
		if ($options ne "")
		{
		    $options .= " ";
		}
		$options .= $items[$i];
	    }
	    $cmds{$cmd}{$items[$i]}{'cnt'} += $items[0];
	    $cmduse{$maincmd}{$items[$i]}{'cnt'} += $items[0];
	    $cmduse{$maincmd}{'cnt'} += $items[0];
	    if ($i <= $#items - 1 && $items[$i+1] !~ /^\-/)
	    {
		$cmds{$cmd}{$items[$i]}{$items[$i+1]} += $items[0];
		$cmduse{$maincmd}{$items[$i]}{$items[$i+1]} += $items[0];
		$i++;
	    }
	}
	else
	{
	    $cmds{$cmd}{'args'}{$items[$i]} += $items[0];
	    $cmduse{$maincmd}{$items[$i]}{'cnt'} += $items[0];
	}
    }
    $cmds{$cmd}{'params'}{$options} += $items[0];
}

open(my $oh, '>', 'cmds.gv') or die "Could not open file cmds.gv  $!";
open(my $ih, '>', 'optargs.gv') or die "Could not open file optargs.gv  $!";
print $oh "digraph G {\n";
print $ih "digraph G {\n";
print $oh "node [shape=record];\n";
print $ih "node [shape=record];\n";
@colors=("#FDDFDF", "#FCF7DE", "#DEFDE0", "#DEF3FD", "#F0DEFD");
    
$sum = 0;
%nodes=();
for $c (sort {$ncs{$b} <=> $ncs{$a}} keys %ncs)
{ 
    @elems = split(/\:/, $c);
    $node = $elems[0];
    $nodecmds{$node} += $ncs{$c};
}
$cntc = 0;
%nodecolors=();
print $oh "node [style=filled, color=\"" . $colors[$cntc%5] . "\"];\n";
print $oh "\"all\" [label=\"all\"]\n";
for $c (sort {$ncs{$b} <=> $ncs{$a}} keys %ncs)
{
    if ($ncs{$c} < 0.01*$all)
    {
	last;
    }
    @elems = split(/\:/, $c);
    $node = $elems[0];
    $maincmd = $elems[1];
    if (!exists($nodes{$node}))
    {
	$cntc++;
	$nodes{$node} = 0;
	$freq=int(100*$nodecmds{$node}/$all)/100;
	$w = $nodecmds{$node}/$all;
	print $oh "node [style=filled, color=\"" . $colors[$cntc%5] . "\"];\n";
	$nodecolors{$node} = $colors[$cntc%5];
	print $oh "all->\"" . $node . "\" [style=\"setlinewidth($w)\", label=$freq]\n";
    }
    $w = $ncs{$c}/$all;
    $freq = int(100*$ncs{$c}/$nodecmds{$node})/100;
    print $oh "node [style=filled, color=\"" . $nodecolors{$node} . "\"];\n";
    print $oh "\"$c\" [label=\"$maincmd\"]\n";
    print $oh "$node->\"" . $c . "\" [style=\"setlinewidth($w)\", label=$freq]\n";
    $printedcmds{$maincmd} = 1;
    if ($c !~ /misspelled/)
    {
	$sumo = 0;
	for $o (sort{$cmds{$c}{'params'}{$b} <=> $cmds{$c}{'params'}{$a}} keys %{$cmds{$c}{'params'}})
	{
	    if ($cmds{$c}{'params'}{$o} < $SMALL*$ncs{$c})
	    {
		last;
	    }
	}
	for $i (sort {$cmds{$c}{$b}{'cnt'} <=> $cmds{$c}{$a}{'cnt'}} keys %{$cmds{$c}})
	{
	    if ($i eq "params")
	    {
		next;
	    }
	    if ($cmds{$c}{$i}{'cnt'} <= $SMALL*$ncs{$c})
	    {
		next;
	    }
	    for $ar (sort {$cmds{$c}{$i}{$b} <=> $cmds{$c}{$i}{$a}} keys %{$cmds{$c}{$i}})
	    {
		if ($ar eq 'cnt')
		{
		    next;
		}
		if ($cmds{$c}{$i}{$ar} < $SMALL*$cmds{$c}{$i}{'cnt'})
		{
		    next;
		}
		print $cmds{$c}{$i}{$ar} . "\t$ar\n";
	    }
	}
	for $ar (sort {$cmds{$c}{'args'}{$b} <=> $cmds{$c}{'args'}{$a}} keys %{$cmds{$c}{'args'}})
	{
	    if ($cmds{$c}{'args'}{$ar} <= $SMALL*$ncs{$c})
	    {
		next;
	    }
	}
    }    
}
# Print out commands and their args
# After 3 commands scroll down
$cntc = 0;
%middle = ();
for $c (keys %cmduse)
{
    if (!exists($printedcmds{$c}))
    {
	next;
    }
    $middle{$cntc} = $c;

    @printi=();
    for $i (sort {$cmduse{$c}{$b}{'cnt'} <=> $cmduse{$c}{$a}{'cnt'}} keys %{$cmduse{$c}})
    {
	if ($i eq 'cnt')
	{
	    next;
	}

	$w = $cmduse{$c}{$i}{'cnt'}/$cmduse{$c}{'cnt'};
	if ($cmduse{$c}{$i}{'cnt'} < $SMALL * $cmduse{$c}{'cnt'})
	{
	    next;
	}
	push(@printi,  escape($c . ":" . $i));
	$frac = int($cmduse{$c}{$i}{'cnt'}/$cmduse{$c}{'cnt'}*100)/100;
	print $ih "node [style=filled, color=\"" . $colors[$cntc%5] . "\"];\n";
	print $ih "\"" . escape($c . ":" . $i) . "\" [label=\"" . escape($i) . "\"]\n";
	print $ih "\"$c\"->\"" . escape($c . ":" . $i) . "\" [style=\"setlinewidth($w)\", label=$frac]\n";
	for $ar (sort {$cmduse{$c}{$i}{$b} <=> $cmduse{$c}{$i}{$a}} keys %{$cmduse{$c}{$i}})
	{
	    if ($ar eq 'cnt')
	    {
		next;
	    }
	    if ($cmduse{$c}{$i}{$ar} < $SMALL * $cmduse{$c}{$i}{'cnt'})
	    {
		next;
	    }
	    $frac = int($cmduse{$c}{$i}{$ar}/$cmduse{$c}{$i}{'cnt'}*100)/100;
	    $w = $cmduse{$c}{$i}{$ar}/$cmduse{$c}{'cnt'};
	    print $ih "\"" . escape($c . ":" . $i . ":" . $ar) . "\" [label=\"" . escape($ar) . "\"]\n";
	    print $ih "\"" . escape($c . ":" . $i) . "\"->\"" . escape($c . ":" . $i . ":" . $ar) . "\" [style=\"setlinewidth($w)\", label=$frac]\n";
	}
    }
    if (scalar(@printi) > 0)
    {
	$middle{$cntc} = $printi[int(scalar(@printi)/2)];
    }

    if ($cntc > 2)
    {
	print $ih "\"" . $middle{$cntc-3} . "\"->\"$c\" [color=\"white\"]\n";
    }
    $cntc ++;
}
print $oh "size=\"7.5,10\"\n}\n";
print $ih "size=\"7.5,10\"\n}\n";
close($oh);
close($ih);
