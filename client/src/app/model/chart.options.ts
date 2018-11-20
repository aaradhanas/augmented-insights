import { DataSet } from "../model/dataset";

export class ChartOptions {
    type:string = 'doughnut';
    labels:string[] = [];
    values:string[] = [];
    datasetLabel:string;
    titleText:string;
    datasets:DataSet[] = [];

    displayLegend:boolean = true;
    legendPosition:string = 'top';
    displayXaxis:boolean = true;
    displayXaxisGridLines:boolean = true;
    displayYaxis:boolean = true;
    displayYaxisGridLines:boolean = true;

    averageValue:number;
}