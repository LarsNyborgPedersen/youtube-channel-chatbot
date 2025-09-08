import { redirect } from 'next/navigation'

export default function HomePage() {
  // Redirect to the channel input page
  redirect('/channel')
}