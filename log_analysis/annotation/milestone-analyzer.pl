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

# This file analyzes milestones. Provide milestone-file 
# folder-w-annotator-output and output-folder

$usage = "$0 milestone-file folders-w-annotator-output output-folder\n";

if ($#ARGV < 2)
{
    print $usage;
    exit(0);
}
%mmet=();
%mattempted=();
%milestones=();
%mattempts=();
%msuccesses=();
%attempts=();
# Load milestones
$fh = new IO::File($ARGV[0]);
$j = 0;
while(<$fh>)
{
    @items = split(/\,/, $_);
    $milestones{$j}{'input'} = $items[1];
    $milestones{$j}{'output'} = $items[2];
    $mattempts{$j} = 0;
    $msuccesses{$j} = 0;
    %{$attempts{$j}} = ();
    $j++;
}
# Load user input and remember attempts and some stats
for ($dir = 1; $dir < $#ARGV; $dir++)
{
    opendir(my $dh, $ARGV[$dir]) || die "Can't open $ARGV[$dir] $!";
    @files = readdir $dh;
    for $f (@files)
    {
	if ($f =~ /^\./)
	{
	    next;
	}
	$fh = new IO::File($ARGV[$dir] . "/" . $f);
	$line = <$fh>;
	#User username start time 1548706268 end 1549309035
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
	    for $e (@elems)
	    {
		if ($e =~ /(^M)(\d+)/)
		{
		    $m = $2;
		    $msuccesses{$m} ++;
		    $mmet{$m}{$uid} = 1;
		}
		elsif ($e =~ /(^A)(\d+)/)
		{
		    $m = $2;
		    $mattempted{$m}{$uid} = 1;
		    $mattempts{$m} ++;
		    $attempts{$m}{$items[5]} = 1;
		}
	    }
	}
    }
}
for $m (sort {$a <=> $b} keys %milestones)
{
    print "Milestone $m input $milestones{$m}{'input'} output $milestones{$m}{'output'} total attempted $mattempts{$m} by " . scalar(keys %{$mattempted{$m}}) . " users, met " . $msuccesses{$m} . "\n";
    $filename = $ARGV[$#ARGV] . "/attempts-" . $m;
    open(my $fh, '>', $filename);
    for $a (keys %{$attempts{$m}})
    {
	print $fh "$a\n";
    }
    close($fh);
}
