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
import {HttpClient} from "@angular/common/http";
import {DragScrollComponent} from "ngx-drag-scroll";
import {Utils} from "../utils/utils";

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent implements AfterViewInit {

  ngAfterViewInit() {
    this.imagesPerScreen = Math.ceil(this.title?.nativeElement.offsetWidth / this.imageWidth) + 1
    this.initialLoad()
  }

  @Output() onSelectedImagesChange: EventEmitter<Set<string>> = new EventEmitter<Set<string>>()
  @Input() folder: string = ""
  @Input() selectionMode: boolean = false
  @ViewChild('nav', {read: DragScrollComponent}) ds: DragScrollComponent | undefined
  @ViewChild('title') title: ElementRef | undefined

  selectedImages: Set<string> = new Set<string>();
  images: Map<string, any> = new Map<string, any>()
  hoveredCheckButton: string = ''
  isHoveredFolder: boolean = false
  hoveredImage: string = ''
  isSelectAll: boolean = false
  isLoading: boolean = false
  dragThreshold: number = 0.8 //to load more items if user beyond (x*100)% of the folder content
  imageWidth = 150
  imagesPerScreen = 0
  unloadedImages: Set<string> = new Set()  //all imageIDs in a folder, load image file as needed later and remove from this set

  constructor(private http: HttpClient) {
  }

  scrolled() {
    let ref: any = this.ds?._contentRef
    const reachedScrollThreshold = ref.nativeElement.scrollLeft + ref.nativeElement.offsetWidth >= this.dragThreshold * ref.nativeElement.scrollWidth;
    if (reachedScrollThreshold) {
      this.loadFiles()
    }
  }

  initialLoad() {
    this.http.get("http://127.0.0.1:5000/folder/" + this.folder).subscribe((files: any) => {
      files.forEach((file: any) => {
          this.unloadedImages.add(file)
        }
      )
      this.loadFiles()
    })
  }

  loadFiles() {
    let loaded = 0
    for (let imageId of this.unloadedImages) {
      if (loaded >= this.imagesPerScreen) break
      this.getImageFromService(imageId)
      loaded++
    }
  }

  getImageFromService(img: string) {
    this.isLoading = true
    let imageFile = new Image()
    imageFile.src = `http://127.0.0.1:5000/image/${this.folder}/${img}`
    this.unloadedImages.delete(img)
    this.images.set(img, imageFile)
    imageFile.onload = (() => {
      this.isLoading = false
    })
  }

  isWideImage(image: string) {
    let img: HTMLImageElement = this.images.get(image)
    return img.width > img.height
  }

  toggleImageSelect(imageId: string) {
    this.selectedImages.has(imageId) ? this.deselectImage(imageId) : this.selectImage(imageId)
    this.selectionChanged()
  }

  isCheckButtonHovered(imageId: string): boolean {
    return this.hoveredCheckButton == imageId
  }

  deselectImage(imageId: string) {
    this.selectedImages.delete(imageId)
    this.isSelectAll = false
  }

  selectImage(imageId: string) {
    this.selectedImages.add(imageId)
    if (this.selectedImages.size == this.images.size) {
      this.isSelectAll = true
    }
  }

  getImageNames(): string[] {
    return Utils.getKeysFromMap(this.images)
  }

  getImageFile(image: string) {
    return this.images.get(image)?.src
  }

  isImageHovered(imageId: string): boolean {
    return this.hoveredImage == imageId
  }

  isImageSelected(imageId: string): boolean {
    return this.isFolderSelected() ? true : this.selectedImages.has(imageId)
  }

  toggleFolderSelect() {
    this.isFolderSelected() ? this.selectedImages.clear() : this.images.forEach(img => this.selectedImages.add(img.name))
    this.isSelectAll = !this.isSelectAll
    this.selectionChanged()
  }

  isFolderSelected() {
    return this.isSelectAll
  }

  selectionChanged() {
    this.onSelectedImagesChange.emit(this.selectedImages)
  }
}
