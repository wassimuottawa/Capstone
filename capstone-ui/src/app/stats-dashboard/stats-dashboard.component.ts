import {Component} from '@angular/core';
import {BackendService} from "../service/backend.service";


@Component({
  selector: 'app-stats-dashboard',
  templateUrl: './stats-dashboard.component.html',
  styleUrls: ['./stats-dashboard.component.css']
})
export class StatsDashboardComponent {

  distributionByTimeIntervalGraph: any
  serviceTimeGraph: any
  serviceTimeDistributionGraph: any
  intervals = ['Breakfast', 'Lunch', 'Snack', 'Dinner', 'Late Night']
  intervalsData: any

  displayedColumns: string[] = ['From', 'To', 'Tickets'];

  constructor(public service: BackendService) {
  }

  onFileChange(event: any) {
    if (event.target.files[0]) {
      const fileReader: any = new FileReader();
      fileReader.readAsText(event.target.files[0], "UTF-8");
      fileReader.onload = () => {
        this.service.generateStats(JSON.parse(fileReader.result)).subscribe(async () => {
          this.service.getTicketsByInterval().subscribe(stats => this.intervalsData = stats)
          await this.getImagePromise(this.service.getDistributionByTimeIntervalGraphSrc()).then((img) => this.distributionByTimeIntervalGraph = img)
          await this.getImagePromise(this.service.getServiceTimeGraphSrc()).then((img) => this.serviceTimeGraph = img)
          await this.getImagePromise(this.service.getServiceTimeDistributionGraphSrc()).then((img) => this.serviceTimeDistributionGraph = img)
        })
      }
    }
  }


  getImagePromise(url: any) {
    return new Promise<any>(resolve => {
      let img = new Image();
      img.src = url;
      img.onload = () => resolve(img);
    });
  }

  getImageFile(image: any) {
    return image?.src
  }
}
