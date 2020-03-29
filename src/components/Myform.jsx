import React from 'react';
import './MyForm.css';
import {  } from '@material-ui/core';

class MyForm extends React.Component {
    constructor(props){ 
      super(props) 
      this.state = { 
          username:'',    // Holds input username
          date:'',        // Holds input date
          time:'',        // Holds input time
          taskname:''     // Holds input taskname
        }
    }

    changeHandler = e =>{
      this.setState({[e.target.name]:e.target.value})
    }
    //State will be set to given input value on changes to the input field

    submitHandler = e =>{         // This function is invoked to submit the input data to the table
      e.preventDefault()          // Prevents browser to refresh
      console.log(this.state) 
      fetch('http://localhost:3001/todo/add',{
        method:'POST',
        mode:'cors',
        headers: {
          "Content-Type": "application/json"
        },
        body:JSON.stringify(this.state)
      })      
      .then(response => response.json())
      .then(res => console.log(res))
      // The request is made to my Flask app's add in order to add data to the To-Do table
    }
    render() { 
      const {username,date,time,taskname} = this.state
      return ( 
        <div>
          <div  className="container">
            <div className="row">
              <div className="col-6">
                <h1>Fill the form to create <br></br>your own TO-DO</h1>
              </div>
              <div className="col-6">
                <div>
                  <form onSubmit={this.submitHandler}>
                    <input type="text" name="username"  value={username} placeholder="Username" onChange={this.changeHandler} required></input>
                    <input type="date" name="date"  value={date} placeholder="Date-of-Task(DD/MM/YYYY)" onChange={this.changeHandler} required></input>
                    <input type="time" name="time"  value={time} placeholder="Time-of-Task(HH:MM),(24 hours)" onChange={this.changeHandler} required></input>
                    <input type="text" name="taskname"  value={taskname} placeholder="Task-Name" onChange={this.changeHandler} required></input>
                    <input className="button" type="submit" value="Add"></input>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
       );
    }
  }
  export default MyForm;

  // MyForm Class comtains Form to add an entry to the table