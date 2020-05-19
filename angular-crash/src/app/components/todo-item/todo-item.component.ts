import { Component, OnInit, Input, EventEmitter,Output } from '@angular/core';
import { Todo } from 'src/app/models/Todo';
import { threadId } from 'worker_threads';
import { TodoService } from '../../services/todo.service'

@Component({
  selector: 'app-todo-item',
  templateUrl: './todo-item.component.html',
  styleUrls: ['./todo-item.component.css']
})
export class TodoItemComponent implements OnInit {

  @Input() todo:Todo;
  @Output() deleteTodo: EventEmitter<Todo> = new EventEmitter();

  constructor(private todoServie:TodoService) { }

  ngOnInit(): void {
  }

  //set dynamic classes
  setClasses(){
    let classes = {
      todo: true,
      'is-complete': this.todo.completed
    }
    return classes;
  }

  //onToggle
  onToggle(todo){
  //    console.log('toggle');
  // toggle in UI
    todo.completed = !todo.completed;
    // toggle on server
    this.todoServie.toggleCompleted(todo).subscribe(todo => console.log(todo));
  }

  onDelete(todo){
    console.log('delete');
    this.deleteTodo.emit(todo);
  }

}
