import { Component } from '@angular/core';
import { ViewEncapsulation } from "@angular/core";
import { OnInit } from "@angular/core";
import { DataService } from "../../services/data.service";
import { RequestOptions } from "@angular/http";
import { Router, ActivatedRoute } from "@angular/router";

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    encapsulation: ViewEncapsulation.None
})

export class HomeComponent implements OnInit{

    files: string[] = [];
    selectedFiles: string[] = [];

    constructor(private dataService:DataService, private router: Router){
        
    }

    ngOnInit(){
        console.log('HomeComponent ngOnInit');
        this.dataService.getUploadedFiles().subscribe(response => {
            this.handleResponse(response);
        });
    }


    fileUpload(event){
        let files:FileList = event.target.files;
        if(files.length > 0){
            let file:File = files[0];
            let formData:FormData = new FormData();
            formData.append('file', file, file.name);
            this.dataService.uploadFile(formData)
                .subscribe(res => {
                    this.dataService.getUploadedFiles().subscribe(response => {
                        this.handleResponse(response);
                    });
                });

       /*      let headers = new Headers();
            headers.append('Content-Type', 'multipart/form-data')
            let requestOptions = new RequestOptions({ headers: headers }); */
        }
    }

    handleResponse(response){
        this.files = [];
        response.forEach(file => {
            this.files.push(file);
        })
    }

    navigateToInsights(fileName){
        sessionStorage.setItem('files', fileName);
        this.router.navigate(['/insights/1']);
    }

    navigateToMergeInsights(){
        sessionStorage.setItem('files', this.selectedFiles.join());
        this.router.navigate(['/insights/1']);
    }

    triggerFileUploadClick(){
        document.getElementById('file-upload').click();
    }

    onCheckboxChecked(event){
        if(event.target.checked){
            this.selectedFiles.push(event.target.value);
        } else{
            let index = this.selectedFiles.indexOf(event.target.value);
            if(index != -1){
                this.selectedFiles.splice(index, 1);
            }
        }
    }
}