import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { DataService } from '../../services/data.service';
import { DataModel } from '../../model/data.model';
import { ChartModel } from '../../model/chart';
import { AfterViewInit } from '@angular/core';
import { ViewEncapsulation } from '@angular/core';
import { AfterContentInit } from '@angular/core';
import { Input } from '@angular/core';
import { OnChanges } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ChartOptions } from 'src/app/model/chart.options';
import { DataSet } from 'src/app/model/dataset';

import 'chartjs-plugin-annotation';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css'],
  encapsulation: ViewEncapsulation.None
})

export class ChartComponent implements OnInit{
  dataModels = [];
  id: string;
  chartIds = [];
  backgroundColors = [
    '#16a085', '#8e44ad', '#2980b9', '#c0392b', '#f39c12'
  ];

  backgroundColors_shuffle = [
    '#f39c12', '#c0392b', '#2980b9', '#8e44ad', '#16a085'
  ];
  borderColors = [
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)'
  ];
  hoverColor = 'd7d7d7';

  constructor() { }

  public ngOnInit() {
  }

  public ngAfterViewInit() {
    console.log('In ngAfterViewInit');
  }

  getChartOptions(chartData, labels, datasets): ChartOptions {
    let options: ChartOptions = new ChartOptions();

    options.type = chartData.type;
    options.labels = labels;
    options.datasets = datasets;
    options.averageValue = chartData.dataAverage;

    switch (chartData.type) {
      case 'horizontalBar':
        options.displayLegend = false;
        options.displayXaxisGridLines = false;
        options.displayYaxisGridLines = false;
        break;
      case 'bar': 
        options.displayXaxisGridLines = false;
        options.displayYaxisGridLines = false;
        break;

      case 'doughnut':
        options.legendPosition = 'right';
        options.displayXaxis = false;
        options.displayYaxis = false;
        break;
    }

    return options;
  }

  // Label and title should be handled
  drawChart(options, chartId, titleText) {
   //console.log('datasets = ', options.datasets);
   Chart.defaults.global.defaultFontFamily = "Josefin Sans";
    let chart = new Chart(chartId, {
      type: options.type,
      data: {
        labels: options.labels,
        datasets: options.datasets
      },
      options: {
        responsive: true,
        legend: {
          display: options.displayLegend,
          position: options.legendPosition
        },
        title: {
          display: true,
          text: titleText,
          fontSize: 18,
          padding:30
        },
        scales: {
          xAxes: [
            {
              display: options.displayXaxis,
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: options.displayXaxisGridLines
              },
              barThickness: 30,
              categorySpacing: 0
            }
          ],
          yAxes: [
            {
              display: options.displayYaxis,
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: options.displayYaxisGridLines
              }
            }
          ]
        }
      }
    });

    return chart;
  }
}
