import logo from './logo.svg';
import './App.css';
import { createClient } from '@supabase/supabase-js';
import { useEffect} from 'react';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Auto dev environments
          
        </h1>
        <SignInWithGithubButton />
      </header>
    </div>
  );
}

const supabase = createClient('https://ymgwygmadbpzlefijsnm.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InltZ3d5Z21hZGJwemxlZmlqc25tIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk3ODE0MjMsImV4cCI6MTk5NTM1NzQyM30.EyODb2ILaFfWg5UnxHFM6GpZtQHcUqoTi8SpRuz-6nM')

export function SignInWithGithubButton() {
  useEffect(() => {
    const { data: authListener } = supabase.auth.onAuthStateChange(
      (event, session) => {
        // Handle session updates
        console.log(event, session)
      }
    )
  }, [])

  const signInWithGithub = async () => {
    const { user, error } = await supabase.auth.signIn({
      provider: 'github'
    })

    if (error) {
      console.log('Error signing in with GitHub:', error.message)
    }
  }

  return (
    <button onClick={signInWithGithub}>
      Sign in with GitHub
    </button>
  )
}

export default App;
