import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-errorbanner',
  templateUrl: './errorbanner.component.html',
  styleUrls: ['./errorbanner.component.less']
})
export class ErrorbannerComponent {

  @Input() message: string;

}
