import React, { useState } from 'react'
import { Link, useHistory } from 'react-router-dom'

import ImageLight from '../assets/img/login-office.jpeg'
import ImageDark from '../assets/img/login-office-dark.png'
import { Label, Input, Button } from '@windmill/react-ui'
import { loginUser } from '../functions/useLogin'

function Login() {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const history = useHistory()
  const handleSubmit = async e => {
    e.preventDefault();    
    const result = await loginUser({
      email,
      password
    });
    if(result.data){
      localStorage.setItem('token', result.data.token);
      history.push('/app/dashboard')
    }
  }

  return (
    <div className="flex items-center min-h-screen p-6 bg-gray-50 dark:bg-gray-900">
      <div className="flex-1 h-full max-w-4xl mx-auto overflow-hidden bg-white rounded-lg shadow-xl dark:bg-gray-800">
        <div className="flex flex-col overflow-y-auto md:flex-row">
          <div className="h-32 md:h-auto md:w-1/2">
            <img
              aria-hidden="true"
              className="object-cover w-full h-full dark:hidden"
              src={ImageLight}
              alt="Office"
            />
            <img
              aria-hidden="true"
              className="hidden object-cover w-full h-full dark:block"
              src={ImageDark}
              alt="Office"
            />
          </div>
          <main className="flex items-center justify-center p-6 sm:p-12 md:w-1/2">
            <div className="w-full">
              <form onSubmit={handleSubmit}>

                <h1 className="mb-4 text-xl font-semibold text-gray-700 dark:text-gray-200">Login</h1>
                <Label>
                  <span>Email</span>
                  <Input className="mt-1" required type="email" placeholder="john@doe.com" onChange={e => setEmail(e.target.value)} />
                </Label>

                <Label className="mt-4">
                  <span>Password</span>
                  <Input className="mt-1" required type="password" placeholder="***************" onChange={e => setPassword(e.target.value)}/>
                </Label>

                <Button type="submit" className="mt-4" block >
                  Log in
                </Button>

           
              </form>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default Login
