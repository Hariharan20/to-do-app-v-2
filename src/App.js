import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import Add from './components/Add'
import Home from './components/Home'
import SimpleTable from './components/Views'
import Edit from './components/Edit'

class App extends React.Component {
  render() {
    return (
      <div>
        <Router>
          <div>
            <Switch>
              <Route path="/" exact component={Home} />
              <Route path="/add" component={Add} />
              <Route path="/view" exact component={SimpleTable}/>
              <Route path="/edit" component={Edit} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;