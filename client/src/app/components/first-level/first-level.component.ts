import { Component, OnInit, Renderer2 } from '@angular/core';
import { DataService } from '../../services/data.service';
import { DataModel } from '../../model/data.model';
import { ChartModel } from '../../model/chart';
import { ViewEncapsulation } from '@angular/core';
import { Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ChartOptions } from 'src/app/model/chart.options';
import { DataSet } from 'src/app/model/dataset';
import { ChartComponent } from "../../components/chart/chart.component";

@Component({
  selector: 'app-first-level',
  templateUrl: './first-level.component.html',
  styleUrls: ['./first-level.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FirstLevelComponent implements OnInit {
  dataModels = [];
  id: string;
  chartIds = [];

  private chart: ChartComponent;
  private level: number;

  constructor(private dataService: DataService,
              private router: Router,
              private renderer2: Renderer2,
              private route: ActivatedRoute) { 
                this.chart = new ChartComponent();
              }

  public ngOnInit() {
      //console.log('files = ', fileNames);
      //Read route param 'level'
      this.readRouteParams();
  }

  readRouteParams(){
    this.route.params.subscribe(params => {
      this.level = +params['level'];
    });
    console.log('level = ', this.level)
    this.getData();

    this.hideInsignificantInsights();
  }

  onActionclicked(event:any){
   const fileNames = sessionStorage.getItem('files');
   let actionElement : HTMLElement;
   if(fileNames.indexOf('Honda') != -1){
      actionElement = document.getElementById('action-automobile'); 
   } else{
      actionElement = document.getElementById('action-analytics'); 
   }
   this.renderer2.addClass(actionElement,'action-show');
  }

  getData(){
    document.getElementById('loading-icon').style.display = 'block';
    if(this.level == 1){
      const fileNames = sessionStorage.getItem('files');
      this.dataService.getLevelOneChartInsights(this.level, fileNames).subscribe(res => {
        document.getElementById('loading-icon').style.display = 'none';
        this.handleResponse(res);
      });
    } else{
      const column = this.route.snapshot.queryParamMap.get('column');
      const value = this.route.snapshot.queryParamMap.get('value');
      this.dataService.getLevelTwoChartInsights(this.level, column, value)
        .subscribe(res => {
          document.getElementById('loading-icon').style.display = 'none';
          this.handleResponse(res);
        });
    }
  }

  hideInsignificantInsights(){
     // TODO Change logic
     this.dataService.onGenerateInsightEvent.subscribe(value => {
      //console.log(value);
      if (value) {
          for (let i = 6; i < this.chartIds.length; i++) {
              document.getElementById('box_' + i).style.display = 'block';
          }
          document.getElementById('box_6').scrollIntoView();
      }
  });
  }

  handleResponse(response) {
    response.forEach(res => {
      const resObj = JSON.parse(res);
      const dataModel = new DataModel();
      dataModel.title = resObj.title;
      if(this.level > 1 ){
        dataModel.insightTitle = resObj.insights[0];
        resObj.insights.splice(0,1)
      }
      dataModel.insights = dataModel.insights.concat(resObj.insights);

      const chartModel = new ChartModel();
      chartModel.data = resObj.chart.data;
      chartModel.dataAverage = resObj.chart.data_average;
      chartModel.columnName = resObj.chart.columnName;
      chartModel.type = resObj.chart.type;

      dataModel.chartData = chartModel;
      this.dataModels.push(dataModel);
    });

    setTimeout(() => { this.displayCharts(); }, 1000);
  }

  handleChartData(model, index) {
    const chartData = model.chartData.data;
    const chartId = 'canvas_' + model.title;
    this.chartIds.push(chartId);

    const labels = [];
    const values = [];
    const valuesMap = new Map();
    const  datasets = [];

    for (var key in chartData) {
      labels.push(key);
      if(typeof chartData[key] === 'object'){
          var obj = chartData[key];
          for(var key in obj){
              let key_values = [];
               if(valuesMap.has(key)){
                key_values = valuesMap.get(key);
               }
               key_values.push(obj[key]);
               valuesMap.set(key, key_values);
          }
      } else{
        values.push(chartData[key]);        
      }
    }

    if(values.length > 0){
      let dataset = new DataSet();
      dataset.label = model.chartData.columnName;
      dataset.data = values.slice(0,5);
      dataset.backgroundColor = this.backgroundColors;
      dataset.borderWidth = 2;
      dataset.borderColors = this.borderColors;
      dataset.hoverBorderColor = this.hoverColor;
      dataset.hoverBorderWidth = 2;
      dataset.fill = false;
      datasets.push(dataset);
    }

    var i = 0;
    valuesMap.forEach((value,key) => {
      let dataset = new DataSet();
      dataset.label = key;
      dataset.data = value;
      dataset.backgroundColor = this.backgroundColors[i];
      dataset.borderWidth = 2;
      dataset.borderColors = this.borderColors;
      dataset.hoverBorderColor = this.hoverColor;
      dataset.hoverBorderWidth = 2;
      dataset.fill = false;
      datasets.push(dataset);
      i++;
    });

    let options = this.chart.getChartOptions(model.chartData, labels.slice(0,5), datasets);
    model.chart = this.chart.drawChart(options, chartId, model.title);
    this.addClickHandler(model.chart, chartId);
    this.addInsignificantInsightsHandler(index, options, values, labels, model.chart);
  }

  /*
    References:
    1. https://stackoverflow.com/questions/44585862/click-event-on-stacked-bar-chart-chartjs
    2. https://jsfiddle.net/u1szh96g/2595/
  */
  addClickHandler(chart, chartId) {
    var canvas = document.getElementById(chartId);
    var component = this;
    if (canvas != null) {
      canvas.onclick = function (event) {
        var activePoints = chart.getElementsAtEvent(event);
        var activePoint = activePoints[0];
        //console.log(activePoint);
        if (activePoint) {
          var chartData = activePoint['_chart'].config.data;
          var selectedIndex = activePoint['_index'];
          var datasetIndex = activePoint._datasetIndex;

          var label = chartData.labels[selectedIndex];
          var value = chartData.datasets[datasetIndex].data[selectedIndex];
          var column = chartData.datasets[datasetIndex].label

          console.log('Selected bar = ' + column +" and value = "+label);
          component.navigatetoNextLevel(column, label);
        }
      }
    }
  }

  addInsignificantInsightsHandler(index, options, values, labels, chart){
    document.getElementById('show_' + index).addEventListener('click', function(){
      options.datasets.forEach(dataset => {
        if (dataset.data.length > 5) {
          dataset.data.splice(5, 10);
        } else {
          values.slice(5, 10).forEach(value => {
            dataset.data.push(value);
          })
        }
      })

      if(options.labels.length > 5){
        options.labels.splice(5, 10);
      } else{
        labels.slice(5, 10).forEach(value => {
          options.labels.push(value);
        })
      }
      chart.update();
    });
  }

  /**
   * Increment the level by 1 and perform navigation
   * @param column
   * @param value 
   */
  navigatetoNextLevel(column, value){
    this.router.navigate(['/insights/'+(this.level+1)], {queryParams: {column: column, value: value}});
    window.location.reload();
  }

  displayCharts() {
    let i = 0;
    this.dataModels.forEach(model => {
      this.handleChartData(model, i);
      if(i > 5){
        document.getElementById('box_'+i).style.display = 'none';
      }
      i++;
    })
  }

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
}
