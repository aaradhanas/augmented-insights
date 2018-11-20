import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { DataService } from './services/data.service';
import { HttpClientModule } from '@angular/common/http';
import { ChartComponent } from './components/chart/chart.component';
import { FooterComponent } from './components/footer/footer.component';
import { HeaderComponent } from './components/header/header.component';
import { HomeComponent } from './components/home/home.component';
import { FirstLevelComponent } from './components/first-level/first-level.component';
import { SecondLevelComponent } from './components/second-level/second-level.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'insights/:level', component: FirstLevelComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    HomeComponent,
    ChartComponent,
    FirstLevelComponent,
    SecondLevelComponent
  ],
  imports: [BrowserModule, HttpClientModule, RouterModule.forRoot(appRoutes)],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule {}
