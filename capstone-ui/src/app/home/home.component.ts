import {
  Component,
  EventEmitter,
  OnChanges,
  Output,
  QueryList,
  SimpleChanges,
  ViewChildren,
  ViewEncapsulation
} from '@angular/core';
import {Utils} from "../utils/utils";
import {FolderComponent} from "../folder/folder.component";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent implements OnChanges {

  ngOnChanges(changes: SimpleChanges) {

  }

  @ViewChildren('folderComponent') folders: QueryList<FolderComponent> = new QueryList<FolderComponent>()
  @Output() onSideMenuClick: EventEmitter<any> = new EventEmitter<any>()

  folderToImagesMap: Map<string, Set<string>> = new Map();
  folderToSelectedImagesMap: Map<string, Set<string>> = new Map();
  selectedFolders: Set<string> = new Set<string>()
  isLoading: boolean = false
  endOfItems: boolean = false
  scrollThreshold: number = 0.8 //if user scrolls beyond (x*100)% of the screen
  lastLoadDate: Date = new Date()
  waitBetweenLoadMore = 500 //1s


  sampleImage1: string = 'https://static01.nyt.com/images/2021/09/14/science/07CAT-STRIPES/07CAT-STRIPES-mediumSquareAt3X-v2.jpg'
  sampleImage2: string = 'https://images.fonearena.com/blog/wp-content/uploads/2013/11/Lenovo-p780-camera-sample-10.jpg'
  sampleImage3: string = 'https://www.gardeningknowhow.com/wp-content/uploads/2017/07/hardwood-tree.jpg'
  sampleImage4: string = 'https://cdn.vox-cdn.com/thumbor/w_NRTaIXZrEriB39pGua86jFAOY=/0x0:1981x2000/1200x800/filters:focal(833x842:1149x1158)/cdn.vox-cdn.com/uploads/chorus_image/image/69021490/m87_lo_april11_polarimetric_average_image_ml_deband_cc_8bit_srgb.0.jpeg'
  sampleImage5: string = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
  sampleImage6: string = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg'
  sampleImage7: string = 'https://img-19.ccm2.net/cI8qqj-finfDcmx6jMK6Vr-krEw=/1500x/smart/b829396acc244fd484c5ddcdcb2b08f3/ccmcms-commentcamarche/20494859.jpg'
  sampleImage8: string = 'https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search/jcr_content/main-pars/image/visual-reverse-image-search-v2_intro.jpg'
  sampleImage9: string = 'https://im0-tub-ru.yandex.net/i?id=84dbd50839c3d640ebfc0de20994c30d&n=27&h=480&w=480'
  sampleImage10: string = 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg'
  sampleImage11: string = 'https://cdn.pixabay.com/photo/2015/04/19/08/32/marguerite-729510__340.jpg'
  sampleImage12: string = 'https://nystudio107-ems2qegf7x6qiqq.netdna-ssl.com/img/blog/_1200x675_crop_center-center_82_line/image_optimzation.jpg'
  sampleImage13: string = 'https://orthostudio.ca/wp-content/uploads/2016/11/image-3.jpg'
  sampleImage14: string = 'https://cdn.pixabay.com/photo/2016/05/05/02/37/sunset-1373171__340.jpg'
  curr = 6


  allImages: string[] = [this.sampleImage1, this.sampleImage2, this.sampleImage3, this.sampleImage4, this.sampleImage5, this.sampleImage6, this.sampleImage7, this.sampleImage8, this.sampleImage9, this.sampleImage10, this.sampleImage11, this.sampleImage12, this.sampleImage13, this.sampleImage14]

  constructor() {
    this.populateSampleData()
  }

  getFolders(): string[] {
    return Utils.getKeysFromMap(this.folderToImagesMap)
  }

  getImages(folder: string): Set<string> {
    return this.folderToImagesMap.get(folder)!
  }

  populateSampleData() {
    this.folderToImagesMap.set('Folder 1', new Set(this.allImages))
    this.folderToImagesMap.set('Folder 2', new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
    this.folderToImagesMap.set('Folder 3', new Set([this.sampleImage4, this.sampleImage1, this.sampleImage2]))
    this.folderToImagesMap.set('Folder 4', new Set([this.sampleImage5, this.sampleImage2, this.sampleImage7]))
    this.folderToImagesMap.set('Folder 5', new Set([this.sampleImage6, this.sampleImage2, this.sampleImage3]))
    this.folderToImagesMap.set('Folder 6', new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
    //this.folderToImagesMap.set('Folder 13', new Set([this.sampleImage6, this.sampleImage2, this.sampleImage3]))
    //this.folderToImagesMap.set('Folder 14', new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
    //this.folderToImagesMap.set('Folder 15', new Set([this.sampleImage4, this.sampleImage1, this.sampleImage2]))
    //this.folderToImagesMap.set('Folder 16', new Set([this.sampleImage5, this.sampleImage2, this.sampleImage7]))
  }

  loadMore() {
    if (this.curr < 20) {
      this.isLoading = true
      console.log("loading..")
      setTimeout(() => {
          this.folderToImagesMap.set('Folder ' + ++this.curr, new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
          this.folderToImagesMap.set('Folder ' + ++this.curr, new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
          this.folderToImagesMap.set('Folder ' + ++this.curr, new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
          this.folderToImagesMap.set('Folder ' + ++this.curr, new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
          this.lastLoadDate = new Date()
          this.isLoading = false
        },
        4000)
    } else {
      this.endOfItems = true
    }
  }

  onScroll(event: any) {
    const scrolledBeyondThreshold = event.target.offsetHeight + event.target.scrollTop >= this.scrollThreshold * event.target.scrollHeight
    if (scrolledBeyondThreshold) {
      let timeFromLastLoad = new Date().getTime() - this.lastLoadDate.getTime()
      if (!this.isLoading && timeFromLastLoad > this.waitBetweenLoadMore) {
        this.loadMore()
      }
    }
  }

  onSelectAllToggle(isSelectAll: boolean, folder: string) {
    isSelectAll ? this.selectedFolders.add(folder) : this.selectedFolders.delete(folder)
  }

  onSelectionChange(selectedImages: Set<string>, folder: string) {
    selectedImages.size ? this.folderToSelectedImagesMap.set(folder, selectedImages) : this.folderToSelectedImagesMap.delete(folder)
  }
}
