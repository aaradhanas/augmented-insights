import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { EventEmitter } from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class DataService {
  url = 'http://localhost:5000';
  onGenerateInsightEvent: EventEmitter<Boolean> = new EventEmitter();
  constructor(private _http: HttpClient) {}

  getLevelOneChartInsights(level, fileNames) {
    return this._http.get(this.url + 
              '/getChartInsights/'+ level +'?fileNames=' + sessionStorage.getItem('files'));
  }

  getLevelTwoChartInsights(level, column, value) {
    return this._http.get(this.url + 
              '/getChartInsights/'+ level + '?column='+column+'&value='+value);
  }

  getUploadedFiles(){
    return this._http.get(this.url + '/files');
  }

  uploadFile(formData){
    console.log('Inside uploadFile');
    return this._http.post(this.url + '/uploadFile', formData);
  }

  onGenerateInsight(){
    this.onGenerateInsightEvent.emit(true);
  }

  deployToZementis(){
    console.log('Inside service deployToZementis')
    return this._http.post(this.url + '/deployToZementis', {});
  }
}
