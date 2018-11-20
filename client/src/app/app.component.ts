import { Component, OnInit, Renderer2 } from '@angular/core';
import { Chart } from 'chart.js';
import { DataService } from './services/data.service';
import { DataModel } from './model/data.model';
import { ChartModel } from './model/chart';
import { Action } from './model/action';
import { AfterViewInit } from "@angular/core";
import { ViewEncapsulation } from "@angular/core";
import { AfterContentInit } from "@angular/core";
import { Input } from "@angular/core";
import { OnChanges } from "@angular/core";
import { ChartOptions } from "src/app/model/chart.options";
import { Router } from "@angular/router";

import * as $ from 'jquery';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})

export class AppComponent implements OnInit, AfterViewInit, AfterContentInit, OnChanges {
  dataModels = [];
  actionsMap = new Map();
  actions = [];

  constructor(private dataService: DataService,
     private router: Router,
     private renderer2: Renderer2) { }

  public ngOnInit() {
    console.log('ngOnInit');
    this.populateActionsMap();
    this.actions.concat(this.getActions());
  }

  public ngAfterContentInit() {
    console.log('ngAfterContentInit');
  }
  public ngOnChanges() {
    console.log('ngOnChanges');
  }

  public ngAfterViewInit() {
    console.log('In ngAfterViewInit');
    this.actions.forEach(action => {
      document.getElementById(action.name+'-icon').getElementsByTagName('use')[0].setAttribute("xlink:href", action.icon);
    })
  }

  isHomePage(){
    return window.location.href.includes('home');
  }

  isDeployVisible(){
    return !window.location.href.includes('home') &&
          !window.location.href.includes('insights/1');
  }

  navigateToHomePage(){
    this.router.navigate(['home']);
  }

  sendSignalToInsightsPage(){
    this.dataService.onGenerateInsight();
  }

  onActionCloseClicked(event:any){
    console.log('onActionCloseClicked');
    const fileNames = sessionStorage.getItem('files');
    let actionElement : HTMLElement;
    if(fileNames.indexOf('Honda') != -1){
       actionElement = document.getElementById('action-automobile'); 
    } else{
       actionElement = document.getElementById('action-analytics'); 
    }
    this.renderer2.removeClass(actionElement,'action-show');
   }

  deployToZementis(){
    console.log('Inside deployToZementis');
    this.dataService.deployToZementis().subscribe(res => {
        console.log(res);
    });
    console.log('After Inside deployToZementis');
  }

  populateActionsMap(){
    let actions = [];
    // Automobile usecase
    actions.push(this.createAction('Contact Dealer', 'agreement'))
    actions.push(this.createAction('Schedule Meeting', 'businessman'))
    this.actionsMap.set('Automobile', actions);

     // Automobile usecase
     actions = []
     actions.push(this.createAction('Network Support', 'agreement'))
     actions.push(this.createAction('Inform team', 'businessman'))
     this.actionsMap.set('Runtime', actions);
  }

  createAction(name, icon){
    let action = new Action();
    action.name = name;
    action.icon = icon;
    return action;
  }

  getActions(){
    const fileNames = sessionStorage.getItem('files');
    console.log('actionsMap = ', this.actionsMap);
    
    return this.actionsMap.get('Automobile');
    /* this.actionsMap.forEach(entry => {
      console.log('key = ', entry.key);
      console.log('fileNames = ', fileNames);
      if (fileNames.indexOf(entry.key) != -1){
        return entry.value;
      } 
    }); */
    
    //return [];
  }

  performAction(number){
    document.getElementById('done-'+number).style.opacity = '1.0';    
  }
}