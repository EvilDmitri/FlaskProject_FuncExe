#! /usr/bin/env python

a = INPUTFIELD_TXT("a_name", "Enter a")
b = INPUTFIELD_TXT("b_name", "Enter b")

c = int(a) + int(b)

OUTPUT_TEXT("title", data=c)
