# Makefile for source rpm: glibc
# $Id$
NAME := glibc
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
