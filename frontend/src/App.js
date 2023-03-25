import './App.css';
import { createClient } from '@supabase/supabase-js';
import { useEffect, useState } from 'react';

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
  const [ isLoggedIn, setLoggedIn ] =  useState(null);
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
  }, [])

  const signInWithGithub = async () => {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'github'
    })

    console.log(data);

    if (error) {
      console.log('Error signing in with GitHub:', error.message)
    }
  }


  if (isLoggedIn) {
    return (
      <div>
        <SetGithubUrl />
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

function SetGithubUrl() {
  const [ githubRepoUrl, setGithubRepoUrl ] = useState(null);


  return (
    <div>
      <input type="text" placeholder='github repo url' value={githubRepoUrl} onChange={e => setGithubRepoUrl(e.target.value)} />
      <button>
        Set Github URL
      </button>
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
