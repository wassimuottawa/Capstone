import {Component, EventEmitter, Input, Output, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent {

  @Output() onSelectedImagesChange: EventEmitter<Set<string>> = new EventEmitter<Set<string>>()
  @Output() onSelectAllToggle: EventEmitter<boolean> = new EventEmitter<boolean>()
  @Input() folder: string = ""
  @Input() images: Set<string> = new Set<string>()

  selectedImages: Set<string> = new Set<string>();
  hoveredCheckButton: string = ''
  isHoveredFolder: boolean = false
  hoveredImage: string = ''
  isSelectAll: boolean = false

  constructor() {
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

  isImageHovered(imageId: string): boolean {
    return this.hoveredImage == imageId
  }

  isImageSelected(imageId: string): boolean {
    return this.isFolderSelected() ? true : this.selectedImages.has(imageId)
  }

  toggleFolderSelect() {
    this.isFolderSelected() ? this.selectedImages.clear() : this.images.forEach(img => this.selectedImages.add(img))
    this.isSelectAll = !this.isSelectAll
    this.onSelectAllToggle.emit(this.isSelectAll)
    this.selectionChanged()
  }

  isFolderSelected() {
    return this.isSelectAll
  }

  selectionChanged() {
    this.onSelectedImagesChange.emit(this.selectedImages)
  }
}
