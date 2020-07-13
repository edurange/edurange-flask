#!/bin/bash
echo "a" > foo.txt
echo "bc" >> foo.txt
echo `id -u` >> foo.txt
chmod 644 foo.txt
more foo.txt | wc
