import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";

@Injectable()
export class HttpService {

  private static SERVICE_URL = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient) {
  }

  getFolders(): Observable<any> {
    return this.http.get(HttpService.SERVICE_URL + "folders")
  }

  getFolderContents(folder: string): Observable<any> {
    return this.http.get(HttpService.SERVICE_URL + "folder/" + folder)
  }

  getImageSrc(folder: string, imageId: string): string {
    return `${HttpService.SERVICE_URL}image/${folder}/${imageId}`
  }

  delete(folderToImages: Map<string, any>) {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin':'*',
        'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers' : '*'
      }),
      body: folderToImages,
    };
    this.http
      .post(`${HttpService.SERVICE_URL}delete`, options)
      .subscribe((s) => {
        console.log(s);
      });
  }

  deleteOne(folder: string, imageId: string): Observable<any> {
    return this.http.delete(`${HttpService.SERVICE_URL}delete/${folder}/${imageId}`)
  }
}
