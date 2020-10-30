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

# Provide one argument, folder with output of annotator

$usage = "$0 folder-w-annotator-output\n";

if ($#ARGV < 0)
{
    print $usage;
    exit(0);
}
%umet=();
%uattempted=();
%users = ();
opendir(my $dh, $ARGV[0]) || die "Can't open $ARGV[0] $!";
@files = readdir $dh;
for $f (@files)
{
    if ($f =~ /^\./)
    {
	next;
    }
    $lines = 0;
    $attempts = 0;
    $miles = 0;
    $fh = new IO::File($ARGV[0] . "/" . $f);
    $line = <$fh>;
    #User username start time 1548706268 end 1549309035
    @items = split /\s+/, $line;
    $uid = $items[1];
    $dur = $items[6] - $items[4];
    <$fh>;
    while(<$fh>)
    {
	if ($_ !~ /^INPUT/)
	{
	    next;
	}
	$isattempt = 0;
	@items = split /\|/, $_;
	@elems = split /\s+/, $items[2];
	for $e (@elems)
	{
	    if ($e =~ /(^M)(\d+)/)
	    {
		$m = $2;
		$umet{$uid}{$m} = 1;
		$miles ++;
	    }
	    elsif ($e =~ /(^A)(\d+)/)
	    {
		$m = $2;
		$uattempted{$uid}{$m} = 1;
		$isattempt = 1;
	    }
	}
	if ($isattempt)
	{
	    $attempts++;
	}
	$lines++;
    }
    $dur = $dur/3600;
    $dur = int($dur*100)/100;
    print "User $uid worked for $dur hours and $lines lines, met " . scalar(keys %{$umet{$uid}}) . " milestones, and attempted " . scalar(keys %{$uattempted{$uid}}) . " total milestone hits $miles and failed attempts $attempts\n";
}

