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

# This file is specific to Deterlab. It pulls logs from the experiment folders
# into one destination folder, and merges them per user

# Arguments are project from which logs are pulled
# and destination folder where they should be saved

$usage="$0 project dst_folder";
if ($#ARGV < 1)
{
    print "$usage\n";
    exit 0;
}
$proj = $ARGV[0];
$dst = $ARGV[1];
%records = ();
opendir(my $dh, "/proj/$proj/logs/output_csv") || die "Can't open exp: $!";
@files = readdir($dh);
for $f (@files)
{
    if ($f =~ /^\./)
    {
	next;
    }
    print "File $f\n";
    if ($f =~ /\.csv/)
    {
	@items = split(/\./, $f);
	$key = $items[0] . "." . $items[1];
	$contents = "";
	$curtime = 0;
	my $fh = new IO::File("/proj/$proj/logs/output_csv/$f");
	while(<$fh>)
	{
	    if ($_ =~ /^CMBEGIN/)
	    {
		if ($curtime > 0)
		{
		    $records{$key}{$curtime} = $contents;
		    $contents = "";
		}
		@elems = split(/\,/, $_);
		$curtime = $elems[2];
	    }
	    $contents .= $_;
	}
	if ($curtime > 0)
	{
	    $records{$key}{$curtime} = $contents;
	}
    }
}
for $key (sort keys %records)
{
    open(my $oh, '>>', $dst . '/' . $key  . '.log');
    for $c (sort {$a <=> $b} keys %{$records{$key}})
    {
	print $oh $records{$key}{$c};
    }
    close($oh);
}
