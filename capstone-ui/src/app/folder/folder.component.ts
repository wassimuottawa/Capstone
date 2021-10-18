import {Component, OnInit, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent implements OnInit {

  constructor() { }

  sampleImages = ['https://static01.nyt.com/images/2021/09/14/science/07CAT-STRIPES/07CAT-STRIPES-mediumSquareAt3X-v2.jpg','https://images.fonearena.com/blog/wp-content/uploads/2013/11/Lenovo-p780-camera-sample-10.jpg', 'https://thumbor.forbes.com/thumbor/960x0/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5db4c7b464b49a0007e9dfac%2FPhoto-of-Maltese-dog%2F960x0.jpg%3Ffit%3Dscale', 'https://www.gardeningknowhow.com/wp-content/uploads/2017/07/hardwood-tree.jpg']
  folders = ['Folder 1', 'Folder 2', 'Folder 3']

  ngOnInit(): void {
  }

}
