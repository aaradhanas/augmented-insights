import { ChartModel } from './chart';
import { Chart } from 'chart.js';

export class DataModel{
    title: string;
    chartData: ChartModel;
    chart: Chart;
    insightTitle: string;
    insights = [];
}
