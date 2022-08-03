import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {HomeComponent} from './home/home.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatOptionModule} from "@angular/material/core";
import {MatButtonModule} from '@angular/material/button';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatMenuModule} from '@angular/material/menu';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatPaginatorModule} from '@angular/material/paginator';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {FolderComponent} from './folder/folder.component';
import {DragScrollModule} from "ngx-drag-scroll";
import {HttpClientModule} from "@angular/common/http";
import {BackendService} from "./service/backend.service";
import {DatePipe} from "@angular/common";
import {TrackletComponent} from './tracklet/tracklet.component';
import {StatsDashboardComponent} from './stats-dashboard/stats-dashboard.component';
import {MatDividerModule} from "@angular/material/divider";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatButtonToggleModule} from "@angular/material/button-toggle";
import {MatTableModule} from "@angular/material/table";

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FolderComponent,
    TrackletComponent,
    StatsDashboardComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatOptionModule,
    MatButtonModule,
    MatInputModule,
    MatSelectModule,
    MatMenuModule,
    MatToolbarModule,
    MatExpansionModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatSnackBarModule,
    MatPaginatorModule,
    ReactiveFormsModule,
    DragScrollModule,
    HttpClientModule,
    MatDividerModule,
    MatSidenavModule,
    MatButtonToggleModule,
    FormsModule,
    MatTableModule,
  ],
  providers: [BackendService, DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule {
}
