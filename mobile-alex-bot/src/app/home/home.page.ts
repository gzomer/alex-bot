// @ts-nocheck
import { Component , OnInit } from '@angular/core';
import { Camera, CameraOptions } from '@ionic-native/camera/ngx';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage implements OnInit {

  	constructor(private camera: Camera) {   		
  	}

  	ngOnInit() {
		let self = this  		

		function getPicture(sourceType){
			const options: CameraOptions = {
			  quality: 10,
			  destinationType: self.camera.DestinationType.DATA_URL,
			  encodingType: self.camera.EncodingType.JPEG,
			  mediaType: self.camera.MediaType.PICTURE,
			  correctOrientation: true,
			  sourceType: sourceType
			}
		    self.camera.getPicture(options).then((imageData) => {			 
			 	window.dispatchEvent(new CustomEvent('pictureData', {detail: imageData}));
			}, (err) => {
				console.log("==> Image error")
				console.log(err)
			});
		}
  		window.addEventListener("takePicture", receiveMessageTakePicture, false);
  		window.addEventListener("choosePicture", receiveMessageChoosePicture, false);

  		function receiveMessageTakePicture(event) {
			getPicture(self.camera.PictureSourceType.CAMERA);
		} 
		function receiveMessageChoosePicture(event) {
			getPicture(self.camera.PictureSourceType.PHOTOLIBRARY);	
		} 
		
  	}

}
