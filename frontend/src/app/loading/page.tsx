'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Loader2 } from 'lucide-react'

export default function LoadingPage() {
  const [progress, setProgress] = useState(0)
  const router = useRouter()

  useEffect(() => {
    // Check if we have a channel URL, if not redirect back
    const searchParams = new URLSearchParams(window.location.search)
    const channelUrl = searchParams.get('channelUrl')
    if (!channelUrl) {
      router.push('/channel')
      return
    }

    // Simulate loading progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          // Navigate to chat page after loading is complete
          setTimeout(() => {
            router.push('/chat')
          }, 500)
          return 100
        }
        return prev + 10
      })
    }, 200)

    return () => clearInterval(interval)
  }, [router])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center">
              <Loader2 className="h-12 w-12 text-blue-600 mx-auto mb-4 animate-spin" />
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Creating Your Chatbot
              </h2>
              <p className="text-gray-600 mb-6">
                Fetching and processing channel content...
              </p>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500">{progress}% complete</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

