$(function() {
	$(chart_id).highcharts({
		title: title,
        subtitle: subtitle,
        xAxis: xAxis,
        yAxis: yAxis,
        legend: legend,
        series: series,
        tooltip: tooltip
	});
});