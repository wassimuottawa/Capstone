import {Component, EventEmitter, Output, ViewEncapsulation} from '@angular/core';
import {Utils} from "../utils/utils";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent {

  @Output() onSideMenuClick: EventEmitter<any> = new EventEmitter<any>()

  folderToImagesMap: Map<string, Set<string>> = new Map();
  folderToSelectedImagesMap: Map<string, Set<string>> = new Map();
  foldersLoading: Set<string> = new Set<string>()
  selectedFolders: Set<string> = new Set<string>()
  allExpanded: boolean = false
  expandAllLoading: boolean = false

  sampleImage1: string = 'https://static01.nyt.com/images/2021/09/14/science/07CAT-STRIPES/07CAT-STRIPES-mediumSquareAt3X-v2.jpg'
  sampleImage2: string = 'https://images.fonearena.com/blog/wp-content/uploads/2013/11/Lenovo-p780-camera-sample-10.jpg'
  sampleImage3: string = 'https://www.gardeningknowhow.com/wp-content/uploads/2017/07/hardwood-tree.jpg'
  sampleImage4: string = 'https://cdn.vox-cdn.com/thumbor/w_NRTaIXZrEriB39pGua86jFAOY=/0x0:1981x2000/1200x800/filters:focal(833x842:1149x1158)/cdn.vox-cdn.com/uploads/chorus_image/image/69021490/m87_lo_april11_polarimetric_average_image_ml_deband_cc_8bit_srgb.0.jpeg'
  sampleImage5: string = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
  sampleImage6: string = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg'
  sampleImage7: string = 'https://img-19.ccm2.net/cI8qqj-finfDcmx6jMK6Vr-krEw=/1500x/smart/b829396acc244fd484c5ddcdcb2b08f3/ccmcms-commentcamarche/20494859.jpg'
  sampleImage8: string = 'https://helpx.adobe.com/content/dam/help/en/stock/how-to/visual-reverse-image-search/jcr_content/main-pars/image/visual-reverse-image-search-v2_intro.jpg'

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
    this.folderToImagesMap.set('Folder 1', new Set([this.sampleImage6, this.sampleImage2, this.sampleImage3]))
    this.folderToImagesMap.set('Folder 2', new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
    this.folderToImagesMap.set('Folder 3', new Set([this.sampleImage4, this.sampleImage1, this.sampleImage2]))
    this.folderToImagesMap.set('Folder 4', new Set([this.sampleImage5, this.sampleImage2, this.sampleImage7]))
  }

  toggleFolderExpansion(isExpanded: boolean, folder: string) {
    this.foldersLoading.add(folder)
    return new Promise(resolve => {
      setTimeout(() => {
          isExpanded ? this.reduceFolder(folder) : this.expandFolder(folder)
          this.foldersLoading.delete(folder)
          resolve(true)
        },
        1500);
    })
  }

  onSelectAllToggle(isSelectAll: boolean, folder: string) {
    isSelectAll ? this.selectedFolders.add(folder) : this.selectedFolders.delete(folder)
  }

  reduceFolder(folder: string) {
    this.folderToImagesMap.set(folder, new Set(Array.from(this.folderToImagesMap.get(folder)!).slice(0, 3)))
  }

  expandFolder(folder: string) {
    [this.sampleImage1, this.sampleImage2, this.sampleImage3, this.sampleImage4, this.sampleImage5, this.sampleImage6, this.sampleImage7, this.sampleImage8].forEach(img => this.folderToImagesMap.get(folder)?.add(img))
  }

  onSelectionChange(selectedImages: Set<string>, folder: string) {
    selectedImages.size ? this.folderToSelectedImagesMap.set(folder, selectedImages) : this.folderToSelectedImagesMap.delete(folder)
  }

  toggleExpandAll() {
    this.expandAllLoading = !this.expandAllLoading
    const promises : any = []
    Array.from(this.folderToImagesMap.keys()).forEach(folder => promises.push(this.toggleFolderExpansion(this.allExpanded, folder)))
    Promise.all(promises).then(() => {
      this.allExpanded = !this.allExpanded
      this.expandAllLoading = !this.expandAllLoading
    })
  }
}
