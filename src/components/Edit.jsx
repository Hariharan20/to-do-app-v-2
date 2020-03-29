import React from 'react';
import './MyForm.css'

class Edit extends React.Component {
    constructor(props){
      super(props)
      this.state = { 
            taskid:'',        // Store taskid received from request
            username:'',      // Store username received from request
            taskdate:'',      // Store taskdate received from request
            tasktime:'',      // Store tasktime received from request
            taskname:'',      // Store taskname received from request
           }
    }
    componentDidMount(){
      let _taskid = '';       // Stores taskid temporarily
      let _taskname='';       // Stores taskname temporarily
      let _username='';       // Stores username temporarily
      let _taskdate='';       // Stores taskdate temporarily
      let _tasktime='';       // Stores tasktime temporarily
      if (localStorage) {     // Values are stored into these variables by parsing into request
            _taskid = JSON.parse(localStorage.getItem('taskid'));
            _username = JSON.parse(localStorage.getItem('username'));
            _tasktime = JSON.parse(localStorage.getItem('tasktime'));
            _taskname = JSON.parse(localStorage.getItem('taskname'));
            _taskdate = JSON.parse(localStorage.getItem('taskdate'));
            console.log(_taskid,_taskname,_tasktime,_taskdate,_username);
            this.setState({username:_username,taskid:_taskid,taskname:_taskname,tasktime:_tasktime,taskdate:_taskdate,});
      }
      this.setState({username:_username,taskid:_taskid,taskname:_taskname,tasktime:_tasktime,taskdate:_taskdate,})
      // States values are set from variable's values
    }

    changeHandler = e =>{
      this.setState({[e.target.name]:e.target.value})
      // Holds state's values
    }
    //State will be set to given input value on changes to the input field

    submitHandler = e =>{     // While submitting the data this function is invoked
      e.preventDefault()
      // prevents the browser to reload
      console.log(this.state) 
      fetch('http://localhost:3001/todo/edit',{
            method:'POST',
            mode:'cors',
            headers: {
            "Content-Type": "application/json"
            },
            body:JSON.stringify(this.state)
      })      
      .then(response => response.json())
      .then(res => console.log(res))
      // fetch is made to my Flask app to store these updated values to the table
    }

    render() { 
      var {username,taskdate,tasktime,taskname} = this.state
      // Values are stored in these variables so that the form can use data from these variables
      console.log("State",this.state)
      return ( 
            <div className="col-8">
                  <div>
                        <form onSubmit={this.submitHandler}>
                              <input type="text" name="username"  value={username} placeholder="Username" onChange={this.changeHandler} required></input>
                              <input type="date" name="taskdate"  value={taskdate} placeholder="Date-of-Task(DD/MM/YYYY)" onChange={this.changeHandler} required></input>
                              <input type="time" name="tasktime"  value={tasktime} placeholder="Time-of-Task(HH:MM),(24 hours)" onChange={this.changeHandler} required></input>
                              <input type="text" name="taskname"  value={taskname} placeholder="Task-Name" onChange={this.changeHandler} required></input>
                              <input className="button" type="submit" value="Add"></input>
                        </form>
                  </div>
            </div>
      );
    }
  }
   
  export default Edit;

  // Edit class is used to edit the data displayed in the table
  // Data needs to be edited is set as this class's state
  // After Editing,this data will be submitted to the Table
  