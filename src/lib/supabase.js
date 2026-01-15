import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = supabaseUrl && supabaseAnonKey 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

export async function addComment(rating, comment) {
  if (!supabase) {
    console.warn('Supabase not configured')
    return { error: 'Supabase not configured' }
  }
  
  const { data, error } = await supabase
    .from('student_comments')
    .insert([{ rating, comment }])
  
  if (error) {
    console.error('Error adding comment:', error)
    return { error: error.message }
  }
  
  return { data }
}
