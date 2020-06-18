#!/usr/bin/env python3
# -*- coding: utf8 -*-

# count-rnils <augmented-filename> [-green]

# provides:
#  absolute top ten stations with most rnils
#  top ten station swith highest percentage of rnils
#  absolute top ten most-busted rnils with Ws
#  top ten stations with highest percentage of rnils with Ws

# 100% generally indicates a problem with the log,
#  so we omit those

# Released under the GNU Public License, version 2

# Principal author: N7DR

# Copyright owner(s):
#    N7DR

import sys

# filename should be an augmented file
filename = sys.argv[1]

# determine the colour of the tables (I use green for CW)
colour = "#99ffff"

if len(sys.argv) > 2:
    if sys.argv[2] == "-green" :
        colour = "#99ff99"

rnil_info = {}

# QSO:  7045 CW 2005-11-27 1154 AA1CA         599 05     FP/K8DD       599 05     AQS1 2154  40 TFFFFFTTFFFFF- -             -             -  -

# number of entries in each table
N_TO_SHOW = 10

# minimum number of QSOs; 50 for one year, 250 for ten years
MIN_QSOS = 250

# determine what constitutes a W; this isn't perfect, but it's good enough for this Q&D python code
def is_w(call, call_zone) :
    call_first_char = call[0]
    call_appears_w = (call_first_char == 'A') or (call_first_char == 'K') or (call_first_char == 'N') or (call_first_char == 'W')
    call_is_w = (call_appears_w and (call_zone == "03" or call_zone == "04" or call_zone == "05"))
    return call_is_w

# here we go
with open(filename) as cabrillo_lines:
  for line in cabrillo_lines:
#    print(line)
    fields = line.split()
    call_1 = fields[5]
    call_1_zone = fields[7]
    
    call_2 = fields[16]         # check for bust first
    if call_2 == "-" :
      call_2 = fields[8]
    
    call_2_zone = fields[10]
    flags = fields[14]
    is_two_way = flags[0] == 'T'
    is_rbust = flags[1] == 'T'
    is_bust = flags[2] == 'T'
    is_nil = flags[4] == 'T'

    if call_2 not in rnil_info:
      rnil_info[call_2] = [0, 0, 0, 0]	# total rQSOs, total rnils, W rQSOs, W rnils 

    rnil_info[call_2][0] += 1		# increment total rQSOs
    
    if is_nil:
      rnil_info[call_2][1] += 1		# increment total rnils if we aren't in his log (accounting for busts)
      
    call_1_is_w = is_w(call_1, call_1_zone)
    call_2_is_w = is_w(call_2, call_2_zone)
      
    if call_1_is_w and call_2_is_w :
      rnil_info[call_2][2] += 1		# increment W rQSOs
      
      if is_nil:
        rnil_info[call_2][3] += 1	# increment W rnils if we are a W and not in his log (accounting for busts)

nrnil_info = []

# require 50 rQSOs; do not include calls with 100% rNILs
for call in rnil_info:
  if rnil_info[call][0] >= MIN_QSOS and rnil_info[call][1] != rnil_info[call][0] :
    nrnil_info.append( ( call,  rnil_info[call][0], rnil_info[call][1], rnil_info[call][2], rnil_info[call][3] ) )

# absolute most rNILS:
most_rnils = sorted(nrnil_info, key = lambda record: record[2], reverse = True)[0:N_TO_SHOW]

print("<table align=\"center\" border=\"2\" cellpadding=\"3\" cellspacing=\"3\" style=\"background-color: " + colour + "; font-family: &quot;courier new&quot; , &quot;courier&quot; , monospace; text-align: center; width: 100%;\">")

print("<tbody>")
print("<tr>\n<th>Callsign</th>\n<th>Total rQSOs</th>\n<th>Total rNILs</th>\n</tr>")
for index in range(0, N_TO_SHOW):
  print("<tr>")
  print(f'<td> {most_rnils[index][0]} </td>')
  print(f'<td> {most_rnils[index][1]} </td>')
  print(f'<td> {most_rnils[index][2]} </td>')
  print("</tr>")

print("</tbody>")
print("</table>")

print("<br/>\n<br/>")

# highest percentage of rNILs
highest_pc_rnils = sorted(nrnil_info, key = lambda record: (100.0 * record[2] / record[1]), reverse = True)[0:N_TO_SHOW]

print("<table align=\"center\" border=\"2\" cellpadding=\"3\" cellspacing=\"3\" style=\"background-color: " + colour + "; font-family: &quot;courier new&quot; , &quot;courier&quot; , monospace; text-align: center; width: 100%;\">")

print("<tbody>")
print("<tr>\n<th>Callsign</th>\n<th>Total rQSOs</th>\n<th>Total rNILs</th>\n<th>% rNILs</th>\n</tr>")
for index in range(0, N_TO_SHOW):
  print("<tr>")
  print(f'<td> {highest_pc_rnils[index][0]} </td>')
  print(f'<td> {highest_pc_rnils[index][1]} </td>')
  print(f'<td> {highest_pc_rnils[index][2]} </td>')
  print(f'<td> {(100 * highest_pc_rnils[index][2] / highest_pc_rnils[index][1]):5.1f} </td>')
  print("</tr>")

print("</tbody>")
print("</table>")

print("<br/>\n<br/>")

# redo for Ws; require 25 rQSOs with Ws; 100% failure with Ws is OK, but still omit global 100% failure
nrnil_info = []

for call in rnil_info :
  if rnil_info[call][2] >= (MIN_QSOS / 2) and rnil_info[call][1] != rnil_info[call][0] :
    nrnil_info.append( ( call,  rnil_info[call][0], rnil_info[call][1], rnil_info[call][2], rnil_info[call][3] ) )

# most rNILs against Ws
w_most_rnils = sorted(nrnil_info, key = lambda record: record[4], reverse = True)[0:N_TO_SHOW]

print("<table align=\"center\" border=\"2\" cellpadding=\"3\" cellspacing=\"3\" style=\"background-color: " + colour + "; font-family: &quot;courier new&quot; , &quot;courier&quot; , monospace; text-align: center; width: 100%;\">")

print("<tbody>")
print("<tr>\n<th>Callsign</th>\n<th>Total rQSOs with Ws</th>\n<th>rNILs against Ws</th>\n</tr>")
for index in range(0, N_TO_SHOW):
  print("<tr>")
  print(f'<td> {w_most_rnils[index][0]} </td>')
  print(f'<td> {w_most_rnils[index][3]} </td>')
  print(f'<td> {w_most_rnils[index][4]} </td>')
  print("</tr>")

print("</tbody>")
print("</table>")

print("<br/>\n<br/>")

# highest percentage of rNILs against Ws
w_highest_pc_rnils = sorted(nrnil_info, key = lambda record: (100.0 * record[4] / record[3]), reverse = True)[0:N_TO_SHOW]

print("<table align=\"center\" border=\"2\" cellpadding=\"3\" cellspacing=\"3\" style=\"background-color: " + colour + "; font-family: &quot;courier new&quot; , &quot;courier&quot; , monospace; text-align: center; width: 100%;\">")

print("<tbody>")
print("<tr>\n<th>Callsign</th>\n<th>Total rQSOs with Ws</th>\n<th>Total rNILs against Ws</th>\n<th>% rNILs against Ws</th>\n</tr>")
for index in range(0, N_TO_SHOW):
  print("<tr>")
  print(f'<td> {w_highest_pc_rnils[index][0]} </td>')
  print(f'<td> {w_highest_pc_rnils[index][3]} </td>')
  print(f'<td> {w_highest_pc_rnils[index][4]} </td>')
  print(f'<td> {(100 * w_highest_pc_rnils[index][4] / w_highest_pc_rnils[index][3]):5.1f} </td>')
  print("</tr>")

print("</tbody>")
print("</table>")

print("<br/>\n<br/>")
