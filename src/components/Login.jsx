import React, { Component } from "react";
import Container from "@material-ui/core/Container";
import "./Login.css";

class Login extends Component {
	constructor(props) {
		super(props);
		this.state = {
                  isToggleOn: true,
                  isValidName :'',
		};
		this.handleSignInSubmit = this.handleSignInSubmit.bind(this);
		this.handleSignUpSubmit = this.handleSignUpSubmit.bind(this);
		this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
		this.setState(state => ({
			isToggleOn: !state.isToggleOn
		}));
	}

	handleErrors(response) {
		if (!response.ok) {
			throw Error(response.statusText);
			// Make a Error Popup
		}
		return response;
	}

	handleSignInSubmit(event) {
		event.preventDefault();
		const data = new FormData(event.target);

		fetch("http://localhost:3001/user/login", {
                  method: "POST",
                  mode: "cors",
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"username": data.get("username"),
				"password": data.get("password")
			})
		})
            .then(response => response.json())
            .then(responseJSON => {console.log(responseJSON)
                  if(responseJSON['noerror']==='valid'){
                        console.log('Vaild user')
                        localStorage.setItem('username',JSON.stringify(responseJSON.username))
                        this.props.history.push({pathname:'/add'})
                  }
            })
            .catch(error => console.log(error));
	}

	handleSignUpSubmit(event) {
		event.preventDefault();
		const data = new FormData(event.target);

		if (data.get("registerPassword") !== data.get("confirmPassword")) {
			// Raise Password Mismatch
                  // Possibly use a Dynamic way to Update and render it
                  console.log("Passwords Mismatch")
			return
		}

		if (
			data.get("registerPassword").length < 5 ||
			data.get("registerName").length < 5
		) {
                  // Raise Length error
                  console.log("Length must be >= 5 characters")
			return
		}
		fetch("http://localhost:3001/user/signup", {
                  method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"username": data.get("registerName"),
				"password": data.get("registerPassword")
			})
		})
			.then(this.handleErrors)
                  .then(response => response.json())
                  .then(responseJSON => console.log(responseJSON))
			.catch(error => console.log(error));
	}

	render() {
		return (
			<Container component="main" maxWidth="md">
				<div className="main-container">
				<div
					className={
						this.state.isToggleOn ? "container" : "container right-panel-active"
					}
					id="container"
				>
				
					<div className="form-container sign-up-container">
						<form className="signup-login" onSubmit={this.handleSignUpSubmit}>
							<h1 className="login-h1">Create Account</h1><br/>
							<input type="text" className="signup-login" name="registerName" placeholder="Username" required />
							<input
							className="signup-login"
								type="password"
								name="registerPassword"
                                                placeholder="Password"
                                                required
							/>
							<input
							className="signup-login"
								type="password"
								name="confirmPassword"
                                                placeholder="Confirm Password"
                                                required
							/>
							<button  action="submit">Sign Up</button>
						</form>
					</div>
					<div className="form-container sign-in-container">
						<form className="signup-login" onSubmit={this.handleSignInSubmit}>
							<h1 className="login-h1">Sign in</h1><br/>
							<input type="text" className="signup-login" name="username" placeholder="Username" required/>
							<input type="password" className="signup-login" name="password" placeholder="Password" required/>
							<a className="forgot-password" href="/forgotPassword.html">Forgot your password?</a>
							<button className="form" action="submit">Sign In</button>
						</form>
					</div>
					<div className="overlay-container">
						<div className="overlay">
							<div className="overlay-panel overlay-left">
								<h1 className="login-h1">Already have an account?</h1>
								<p className="slide-content">Hop in.</p>
								<button
									className="ghost"
									onClick={this.handleClick}
									id="signIn"
								>
									Sign In
								</button>
							</div>
							<div className="overlay-panel overlay-right">
								<h1 className="login-h1">New to To-Do?</h1>
								<p className="slide-content">Create a new account for the best experience.</p>
								<button
									className="ghost"
									onClick={this.handleClick}
									id="signUp"
								>
									Sign Up
								</button>
							</div>
						</div>
					</div>
				</div>
				</div>
			</Container>
		);
	}
}

export default Login;
