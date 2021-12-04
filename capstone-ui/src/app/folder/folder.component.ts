import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild,
  ViewEncapsulation
} from '@angular/core';
import {DragScrollComponent} from "ngx-drag-scroll";
import {Utils} from "../utils/utils";
import {HttpService} from "../service/HttpService";
import { DatePipe } from '@angular/common'

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent implements AfterViewInit {

  ngAfterViewInit() {
    this.imagesPerRow = Math.ceil(this.title?.nativeElement.offsetWidth / this.imageWidth) + 1
    this.initialLoad()
  }

  @Output() onSelectedImagesChange: EventEmitter<Set<string>> = new EventEmitter<Set<string>>()
  @Input() folder: string = ""
  @Input() selectionMode: boolean = false
  @ViewChild('nav', {read: DragScrollComponent}) ds: DragScrollComponent | undefined
  @ViewChild('title') title: ElementRef | undefined

  selectedImagesIds: Set<string> = new Set<string>();
  imageIdToImageMap: Map<string, any> = new Map<string, any>()
  hoveredCheckButtonId: string = ''
  isHoveredFolder: boolean = false
  hoveredImageId: string = ''
  isSelectAll: boolean = false
  isLoading: boolean = false
  dragThreshold: number = 0.8 //to load more items if user beyond (x*100)% of the folder content
  imageWidth = 150
  imagesPerRow = 0 //Will be calculated based on the width of the screen, this is used to know how many images to preload, when user scrolls beyond @dragThreshold a count of @imagesPerRow will be loaded more
  unloadedImages: Set<string> = new Set()  //all imageIDs in a folder, load image file as needed later and remove from this set

  constructor(private service: HttpService, private datePipe : DatePipe) {
  }

  onScroll() {
    let ref: any = this.ds?._contentRef
    const reachedScrollThreshold = ref.nativeElement.scrollLeft + ref.nativeElement.offsetWidth >= this.dragThreshold * ref.nativeElement.scrollWidth;
    if (reachedScrollThreshold) {
      this.loadFiles()
    }
  }

  initialLoad() {
    this.service.getFolderContents(this.folder).subscribe((files: any) => {
      files.forEach((file: any) => {
          this.unloadedImages.add(file)
        }
      )
      this.loadFiles()
    })
  }

  refreshContent() {
    console.log("refreshing" + this.folder)
    this.selectedImagesIds.clear()
    this.imageIdToImageMap.clear()
    this.unloadedImages.clear()
    this.initialLoad()
  }

  getDate(imageId : string) : string {
    return this.datePipe.transform(new Date(parseInt(imageId.split(".")[0])*1000), 'hh:mm:ss') ?? ""
  }

  deleteSelected() {
    this.selectedImagesIds.forEach(img => {
      this.imageIdToImageMap.delete(img)
      this.unloadedImages.delete(img)
    })
    this.selectedImagesIds.clear()
  }

  loadFiles() {
    let loaded = 0
    for (let imageId of this.unloadedImages) {
      if (loaded >= this.imagesPerRow) break
      this.getImageFromService(imageId)
      loaded++
    }
  }

  getImageFromService(imageId: string) {
    this.isLoading = true
    let imageFile = new Image()
    imageFile.src = this.service.getImageSrc(this.folder, imageId)
    this.unloadedImages.delete(imageId)
    this.imageIdToImageMap.set(imageId, imageFile)
    imageFile.onload = (() => {
      this.isLoading = false
    })
  }

  isWideImage(image: string) {
    let img: HTMLImageElement = this.imageIdToImageMap.get(image)
    return img.width > img.height
  }

  toggleImageSelect(imageId: string) {
    this.selectedImagesIds.has(imageId) ? this.deselectImage(imageId) : this.selectImage(imageId)
    this.selectionChanged()
  }

  isCheckButtonHovered(imageId: string): boolean {
    return this.hoveredCheckButtonId == imageId
  }

  deselectImage(imageId: string) {
    this.selectedImagesIds.delete(imageId)
    this.isSelectAll = false
  }

  selectImage(imageId: string) {
    this.selectedImagesIds.add(imageId)
    if (this.selectedImagesIds.size == this.imageIdToImageMap.size) {
      this.isSelectAll = true
    }
  }

  getImageNames(): string[] {
    return Utils.getKeysFromMap(this.imageIdToImageMap)
  }

  getImageFile(image: string) {
    return this.imageIdToImageMap.get(image)?.src
  }

  isImageHovered(imageId: string): boolean {
    return this.hoveredImageId == imageId
  }

  isImageSelected(imageId: string): boolean {
    return this.isFolderSelected() ? true : this.selectedImagesIds.has(imageId)
  }

  toggleFolderSelect() {
    this.isFolderSelected() ? this.deselectAll() : this.imageIdToImageMap.forEach(img => this.selectedImagesIds.add(img.name))
    this.isSelectAll = !this.isSelectAll
    this.selectionChanged()
  }

  deselectAll() {
    this.selectedImagesIds.clear()
  }

  isFolderSelected() {
    return this.isSelectAll
  }

  selectionChanged() {
    this.onSelectedImagesChange.emit(this.selectedImagesIds)
  }
}
