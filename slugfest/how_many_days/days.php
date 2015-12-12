<?php
date_default_timezone_set('PRC');

function daysMonth($year, $month) {
	$r = array(29, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	$m = ($month == 2 && ($year%4==0&&$year%100!=0)||($year%400==0)) ? 0 : $month;
	return $r[$m];
}

function f($date, $md)
{
	$begin = strtotime($date);
	$d = date_parse($date);
	$m = mktime(0, 0, 0, $d['month'], 1, $d['year']);
	$u = strtotime("+ 1 Months", $m);
	$n = date_parse(date("Y-m-d", $u));
	$min = min($d['day'], daysMonth($n['year'], $n['month']));
	$end = $u + ($min - 1) * 3600 * 24;
	return ($end - $begin) / 3600 / 24;
}

echo f('2016-2-10', 1) . ' Days';
echo "\n";