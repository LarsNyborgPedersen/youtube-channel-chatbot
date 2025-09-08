'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Youtube, MessageCircle } from 'lucide-react'

export default function ChannelPage() {
  const [channelUrl, setChannelUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleCreateChatbot = async () => {
    if (!channelUrl.trim() || !isValidYouTubeUrl(channelUrl)) return
    
    setIsLoading(true)
    
    // Use React state management instead of sessionStorage
    // The URL will be passed as a query parameter to the next page
    router.push(`/loading?channelUrl=${encodeURIComponent(channelUrl)}`)
  }

  const isValidYouTubeUrl = (url: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(c\/|channel\/|@)|youtu\.be\/)/
    return youtubeRegex.test(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Youtube className="h-8 w-8 text-red-600" />
              <h1 className="text-3xl font-bold text-gray-900">
                YouTube Channel Q&A
              </h1>
            </div>
            <p className="text-gray-600">
              Ask questions about any YouTube channel's content
            </p>
          </div>

          {/* Channel Input Form */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-6">
              <MessageCircle className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Create Your Chatbot
              </h2>
              <p className="text-gray-600">
                Enter a YouTube channel URL to create a chatbot that can answer questions about its content
              </p>
            </div>
            
            <div className="space-y-4">
              <div>
                <label htmlFor="channel-url" className="block text-sm font-medium text-gray-700 mb-2">
                  YouTube Channel URL
                </label>
                <Input
                  id="channel-url"
                  type="url"
                  placeholder="https://www.youtube.com/@channelname or https://www.youtube.com/c/channelname"
                  value={channelUrl}
                  onChange={(e) => setChannelUrl(e.target.value)}
                  className="w-full"
                />
                {channelUrl && !isValidYouTubeUrl(channelUrl) && (
                  <p className="text-sm text-red-600 mt-1">
                    Please enter a valid YouTube channel URL
                  </p>
                )}
              </div>
              
              <Button
                onClick={handleCreateChatbot}
                disabled={!channelUrl.trim() || !isValidYouTubeUrl(channelUrl) || isLoading}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Creating...' : 'Create Chatbot'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

