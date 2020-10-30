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

# Analyzes one folder, creates a folder with summary for each 
# milestone and for U labels

$usage = "$0 milestone-file folder-w-annotator-output\n";

if ($#ARGV < 1)
{
    print $usage;
    exit(0);
}
%mmet=();
%mattempted=();
%milestones=();
%mattempts=();
%attempts=();
%successes=();
%unrelated = ();
# Load milestones
$fh = new IO::File($ARGV[0]);
$j = 0;
while(<$fh>)
{
    @items = split(/\,/, $_);
    $milestones{$j}{'input'} = $items[1];
    $milestones{$j}{'output'} = $items[2];
    $mattempts{$j} = 0;
    %{$attempts{$j}} = ();
    %{$successes{$j}} = ();
    $j++;
}
$output = "analyzed";
print "Making $output";
system("mkdir $output");
$filename = $output . "/all";
open(my $ah, '>', $filename);
$filename = $output . "/unique-successes";
open(my $ush, '>', $filename);
$filename = $output . "/unique-attempts";
open(my $uah, '>', $filename);
$filename = $output . "/unique-unrelated";
open(my $uuh, '>', $filename);
# Load user input and remember attempts and some stats
$all = 0;
$su = 0;
$fa = 0;
$un = 0;
$uun = 0;
$ufa = 0;
$usu = 0;
$users = 0;
%unique=();
%uniqueattempts=();
%uniqueunrelated=();
%uniquesuccesses=();
$dir = $ARGV[1];
opendir(my $dh, $dir) || next;
@files = readdir $dh;
for $f (@files)
{
    if ($f =~ /^\./)
    {
	next;
    }
    $fh = new IO::File($dir . "/" . $f);
    $line = <$fh>;
    $users++;
	
    @items = split /\s+/, $line;
    $uid = $items[1];
    <$fh>;
    while(<$fh>)
    {
	if ($_ !~ /^INPUT/)
	{
	    next;
	}
	@items = split /\|/, $_;
	@elems = split /\s+/, $items[2];
	$all++;
	print $ah $items[5] . " " . $items[1] . "\n";
	$added = 0;
	if (!exists($unique{$items[5]}))
	{
	    $added = 1;
	    $unique{$items[5]} = 0;
	}
	$unique{$items[5]} ++;
	$fs = 0;
	$ff = 0;
	for $e (@elems)
	{
	    if ($e =~ /(^M)(\d+)/)
	    {
		$m = $2;
		$mmet{$m}{$uid} = 1;
		$successes{$m}{$items[5]} = $items[1];
		if (!exists($uniquesuccesses{$items[5]}))
		{
		    $uniquesuccesses{$items[5]} = 0;
		}
		$uniquesuccesses{$items[5]} ++;
		$fs = 1;
	    }
	    elsif ($e =~ /(^A)(\d+)/)
	    {
		$m = $2;
		$mattempted{$m}{$uid} = 1;
		$mattempts{$m} ++;
		$attempts{$m}{$items[5]} = $items[1];
		if (!exists($uniqueattempts{$items[5]}))
		{
		    $uniqueattempts{$items[5]} = 0;
		}
		$uniqueattempts{$items[5]} ++;
		$ff = 1;
	    }
	    elsif ($e =~ /U/)
	    {
		$unrelated{$items[5]} = $items[1];
		$u++;
		if ($added)
		{
		    $uu++;
		}
		if (!exists($uniqueunrelated{$items[5]}))
		{
		    $uniqueunrelated{$items[5]} = 0;
		}
		$uniqueunrelated{$items[5]} ++;
	    }
	}
	if ($fs == 1)
	{
	    $su++;
	    if ($added)
	    {
		$usu++;
	    }
	}
	elsif ($ff == 1)
	{
	    $fa++;
	    if ($added)
	    {
		$ufa++;
	    }
	}
    }
}
print "All $all successes $su failures $fa unrelated $u users $users unique " . scalar(keys %unique) . " successes $usu failures $ufa unrelated $uu\n";

$filename =  $output . "/unrelated";
open(my $fh, '>', $filename);
for $a (keys %unrelated)
{
    print $fh "$a " . $unrelated{$a} . "\n";
}
close($fh);
for $m (sort {$a <=> $b} keys %milestones)
{
    print "Milestone $m input $milestones{$m}{'input'} output $milestones{$m}{'output'} total attempted $mattempts{$m} by " . scalar(keys %{$mattempted{$m}}) . " users\n";
    $filename =  $output . "/attempts-" . $m;
    open(my $fh, '>', $filename);
    for $a (keys %{$attempts{$m}})
    {
    print $fh "$a " . $attempts{$m}{$a} . "\n";
    }
    close($fh);
    $filename =  $output . "/successes-" . $m;
    open(my $fh, '>', $filename);
    for $a (keys %{$successes{$m}})
    {
    print $fh "$a " . $successes{$m}{$a} . "\n";
    }
    close($fh);
}
for $a (keys %uniquesuccesses)
{
    print $ush $uniquesuccesses{$a} . " $a\n";
}
for $a (keys %uniqueattempts)
{
    print $uah $uniqueattempts{$a} . " $a\n";
}
for $a (keys %uniqueunrelated)
{
    print $uuh $uniqueunrelated{$a} . " $a\n";
}

