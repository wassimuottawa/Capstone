import {ChangeDetectionStrategy, Component, ViewEncapsulation} from '@angular/core';
import {Utils} from "../utils/utils";

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent {

  constructor() {
    this.folderToImagesMap.set('Folder 1', new Set([this.sampleImage1, this.sampleImage2, this.sampleImage3]))
    this.folderToImagesMap.set('Folder 2', new Set([this.sampleImage2, this.sampleImage4, this.sampleImage7]))
    this.folderToImagesMap.set('Folder 3', new Set([this.sampleImage4, this.sampleImage1, this.sampleImage2]))
    this.folderToImagesMap.set('Folder 4', new Set([this.sampleImage5, this.sampleImage2, this.sampleImage7]))
  }

  selectedImages: Set<string> = new Set<string>();
  expandedFolders: Set<string> = new Set<string>();
  folderToImagesMap: Map<string, Set<string>> = new Map();
  hoveredCheckButton: [string, string] = ['', '']
  hoveredFolder: string = ''
  folderToSelectedImagesMap: Map<string, Set<string>> = new Map();


  hoveredImage: [string, string] = ['', '']
  sampleImage1: string = 'https://static01.nyt.com/images/2021/09/14/science/07CAT-STRIPES/07CAT-STRIPES-mediumSquareAt3X-v2.jpg'
  sampleImage2: string = 'https://images.fonearena.com/blog/wp-content/uploads/2013/11/Lenovo-p780-camera-sample-10.jpg'
  sampleImage3: string = 'https://www.gardeningknowhow.com/wp-content/uploads/2017/07/hardwood-tree.jpg'
  sampleImage4: string = 'https://cdn.vox-cdn.com/thumbor/w_NRTaIXZrEriB39pGua86jFAOY=/0x0:1981x2000/1200x800/filters:focal(833x842:1149x1158)/cdn.vox-cdn.com/uploads/chorus_image/image/69021490/m87_lo_april11_polarimetric_average_image_ml_deband_cc_8bit_srgb.0.jpeg'
  sampleImage5: string = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
  sampleImage6: string = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg'
  sampleImage7: string = 'https://img-19.ccm2.net/cI8qqj-finfDcmx6jMK6Vr-krEw=/1500x/smart/b829396acc244fd484c5ddcdcb2b08f3/ccmcms-commentcamarche/20494859.jpg'


  selectImage(folder: string, imageID: string) {
    if (this.isImageSelected(folder, imageID)) {
      this.folderToSelectedImagesMap.get(folder)?.delete(imageID)
      if (this.folderToSelectedImagesMap.get(folder)?.size == 0) {
        this.folderToSelectedImagesMap.delete(folder)
      }
    } else {
      if (this.folderToSelectedImagesMap.has(folder)) {
        this.folderToSelectedImagesMap.get(folder)?.add(imageID)
      } else {
        this.folderToSelectedImagesMap.set(folder, new Set<string>())
        this.folderToSelectedImagesMap.get(folder)?.add(imageID)
      }
    }
  }

  isCheckButtonHovered(folder: string, image: string): boolean {
    return Utils.equalTuples(this.hoveredCheckButton, [folder, image])
  }

  isImageHovered(folder: string, image: string): boolean {
    return Utils.equalTuples(this.hoveredImage, [folder, image])

  }

  isImageSelected(folder: string, imageId: string): boolean {
    return this.folderToSelectedImagesMap.get(folder)?.has(imageId) == true
  }

  selectFolder(folder: string) {
    if (this.isFolderSelected(folder)) {
      this.folderToSelectedImagesMap.delete(folder)
    } else {
      this.folderToSelectedImagesMap.set(folder, new Set<string>(this.folderToImagesMap.get(folder)))
    }
  }

  isFolderSelected(folder: string) {
    return this.folderToSelectedImagesMap.get(folder)?.size == this.folderToImagesMap.get(folder)?.size
  }

  expandOrReduceFolder(folder: string) {
    this.expandedFolders.has(folder) ? this.reduceFolder(folder) : this.expandFolder(folder)
  }

  reduceFolder(folder: string) {
    this.folderToImagesMap.set(folder, new Set(Array.from(this.folderToImagesMap.get(folder)!).slice(0, 3)))
    this.expandedFolders.delete(folder)
  }

  expandFolder(folder: string) {
    [this.sampleImage1, this.sampleImage2, this.sampleImage3, this.sampleImage4, this.sampleImage5, this.sampleImage6, this.sampleImage7].forEach(img => this.folderToImagesMap.get(folder)?.add(img))
    this.expandedFolders.add(folder)
  }


}
