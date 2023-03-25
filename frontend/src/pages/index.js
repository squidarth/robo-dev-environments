import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import { createClient } from '@supabase/supabase-js'


const inter = Inter({ subsets: ['latin'] })

// const supabase = createClient('YOUR_SUPABASE_URL', 'YOUR_SUPABASE_PUBLIC_KEY')

export default function Home() {
  return (
    <>
      <Head>
        <title>Auto Dev Environment</title>
        <meta name="description" content="Automatically make a dev environment" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <h1>Auto Dev Environments!</h1>
      </main>
    </>
  )
}

/** 
export function SignInWithGithubButton() {
  useEffect(() => {
    const { data: authListener } = supabase.auth.onAuthStateChange(
      (event, session) => {
        // Handle session updates
        console.log(event, session)
      }
    )

    // Cleanup auth listener
    return () => {
      authListener.unsubscribe()
    }
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
*/