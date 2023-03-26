import './App.css';
import { createClient } from '@supabase/supabase-js';
import { useEffect, useState } from 'react';
import axios from 'axios';



const isDevelopment = false;

var backendUrl = "";

if (isDevelopment) {
  backendUrl = "http://localhost:4000"
}

const supabase = createClient('https://ymgwygmadbpzlefijsnm.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InltZ3d5Z21hZGJwemxlZmlqc25tIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk3ODE0MjMsImV4cCI6MTk5NTM1NzQyM30.EyODb2ILaFfWg5UnxHFM6GpZtQHcUqoTi8SpRuz-6nM')

function App() {
  return (
    <div className="App">
        <h1>
          Auto dev environments
          
        </h1>
        <Github />
    </div>
  );
}


export function Github() {
  const [ sessionData, setLoggedIn ] =  useState(null);
  useEffect(() => {
     supabase.auth.onAuthStateChange(
      (event, session) => {
        // Handle session updates
        if (event === 'SIGNED_IN') {
          console.log('signed in')
        }
        if (session !== null) {
          setLoggedIn(session)
        }
        console.log(event, session)
      }
    )
  }, [setLoggedIn])

  const signInWithGithub = async () => {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github',
      options: {
        scopes: "codespace,repo",
      }
    })

    console.log(data);

    if (error) {
      console.log('Error signing in with GitHub:', error.message)
    }
  }


  if (sessionData) {
    return (
      <div>
        <SetGithubUrl accessToken={sessionData.access_token} email={sessionData.user.email} />
        <SignOut />
      </div>
    );
    

  } else {
    return (
      <button onClick={signInWithGithub}>
        Sign in with GitHub
      </button>
    )
  }
}

function SetGithubUrl(props) {
  const [ githubRepoUrl, setGithubRepoUrl ] = useState(null);
  const [ triggeredGithubUrl, setTriggeredGithubUrl ] = useState(null);

  function createDevEnvironment(githubRepoUrl) {
    axios.post(backendUrl + "/create-dev-environment", {"githubRepoUrl": githubRepoUrl, "githubAccessToken": props.accessToken, "email": props.email }).then((response) => {
      setTriggeredGithubUrl(githubRepoUrl);
    })
  }

  var triggeredGithubUrlText = null;

  if (triggeredGithubUrl) {
    triggeredGithubUrlText = (
      <p>
        Setting up dev environment for {triggeredGithubUrl}
      </p>
    )
  }


  return (
    <div>
      <input type="text" placeholder='github repo url' value={githubRepoUrl} onChange={e => setGithubRepoUrl(e.target.value)} />
      <button onClick={() => createDevEnvironment(githubRepoUrl)}>
        Set Github URL
      </button>
      {triggeredGithubUrlText}
    </div>
  )
}



function SignOut() {
  const signOut = async () => {
    const { error } = await supabase.auth.signOut()

    if (error) {
      console.log('Error signing out:', error.message)
    }
  }

  return (
    <p>
      <button onClick={signOut}>
        Sign out
      </button>
    </p>

  )
} 

export default App;
