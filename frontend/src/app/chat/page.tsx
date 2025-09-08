'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ArrowLeft, MessageCircle } from 'lucide-react'

export default function ChatPage() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [channelUrl, setChannelUrl] = useState('')
  const router = useRouter()

  useEffect(() => {
    // Get channel URL from sessionStorage
    const storedChannelUrl = sessionStorage.getItem('channelUrl')
    if (!storedChannelUrl) {
      router.push('/channel')
      return
    }
    setChannelUrl(storedChannelUrl)
  }, [router])

  const handleAskQuestion = () => {
    if (!question.trim()) return
    
    // Placeholder answer for now
    setAnswer('Answer placeholder - this will be replaced with real AI responses in later steps.')
  }

  const handleBack = () => {
    router.push('/channel')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <MessageCircle className="h-8 w-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900">
                Channel Chatbot
              </h1>
            </div>
            <p className="text-gray-600">
              Ask questions about the channel's content
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <Button
                variant="outline"
                onClick={handleBack}
                className="flex items-center gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
              <div className="text-sm text-gray-500 truncate max-w-xs">
                Channel: {channelUrl}
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                  Ask a Question
                </h2>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                      Your Question
                    </label>
                    <Textarea
                      id="question"
                      placeholder="What would you like to know about this channel's content?"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      className="min-h-[100px]"
                    />
                  </div>
                  
                  <Button
                    onClick={handleAskQuestion}
                    disabled={!question.trim()}
                    className="w-full"
                    size="lg"
                  >
                    Ask Question
                  </Button>
                </div>
              </div>

              {answer && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Answer
                  </h3>
                  <div className="bg-gray-50 rounded-lg p-4 border">
                    <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

