import Renderer from './services/Renderer'
import { useState, useEffect } from 'react'
import * as jsonpatch from 'fast-json-patch'

let server_data = {
  root: {
    type: 'root',
    children: [
      {
        type: 'container',
        variant: 'vertical',
        children: [
          {
            type: 'text',
            variant: 'header',
            value: 'Product Catalog',
          },
          {
            type: 'container',
            variant: 'horizontal',
            children: [
              {
                type: 'list',
                children: [
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://dummyimage.com/340x520',
                        alt: 'Phone',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Phone',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $8',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Alone art class size pull where improve drive change seem without leg against.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://placekitten.com/653/601',
                        alt: 'Consumer',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Consumer',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $52',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Rather various reach above type bit southern.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://placekitten.com/965/461',
                        alt: 'Everything',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Everything',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $5',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Drop product industry hundred system example couple attack.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://placekitten.com/227/383',
                        alt: 'Stage',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Stage',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $1',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Dinner investment seem probably call marriage gas first program stop act.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://dummyimage.com/221x23',
                        alt: 'Matter',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Matter',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $24',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Build economic future prove they pass couple seem avoid final.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/910/85',
                        alt: 'Second',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Second',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $54',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Southern great magazine marriage church throughout end I somebody.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://placekitten.com/133/212',
                        alt: 'Than',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Than',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $67',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'At paper build card including cover you talk.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/964/1019',
                        alt: 'Better',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Better',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $29',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Soon off special factor organization current power little something available information case individual.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/880/385',
                        alt: 'About',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'About',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $47',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Laugh participant worker American character public section book law pressure read drop.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/629/485',
                        alt: 'From',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'From',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $98',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Truth hospital season five show store management now trial some.',
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            type: 'text',
            variant: 'header',
            value: 'Top 5 Products by Customer Ratings',
          },
          {
            type: 'container',
            variant: 'horizontal',
            children: [
              {
                type: 'list',
                children: [
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/29/503',
                        alt: 'Particularly',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Particularly',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $68',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Units Sold: 703',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Prove social put born want sort.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://dummyimage.com/632x352',
                        alt: 'Environmental',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Environmental',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $62',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Units Sold: 495',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Per professor food agency young treatment.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://dummyimage.com/538x310',
                        alt: 'Campaign',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Campaign',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $95',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Units Sold: 400',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Peace training bring condition glass office leader center mission member everyone season bank.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://picsum.photos/380/377',
                        alt: 'Skin',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Skin',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $40',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Units Sold: 319',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Receive sister generation because thank college dark.',
                      },
                    ],
                  },
                  {
                    type: 'container',
                    variant: 'vertical',
                    children: [
                      {
                        type: 'image',
                        src: 'https://placekitten.com/973/464',
                        alt: 'Exist',
                      },
                      {
                        type: 'text',
                        variant: 'subheader',
                        value: 'Exist',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Price: $56',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value: 'Units Sold: 60',
                      },
                      {
                        type: 'text',
                        variant: 'paragraph',
                        value:
                          'Throw develop show fire recognize pick capital cause everyone hand.',
                      },
                    ],
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        type: 'button',
        label: 'Load More Products',
        action: 'load_more_products',
      },
    ],
  },
}

function App() {
  const [currentUISpec, setUiSpec] = useState({})
  const [prompt, setPrompt] = useState('')
  const [llmStatusMessage, setLlmStatusMessage] = useState('')

  // useEffect(() => {
  //   const src = new EventSource('http://127.0.0.1:8000/ui_stream_patch')

  //   src.addEventListener('end', () => {
  //     console.log('Stream ended. Closing SSE.')
  //     src.close()
  //   })

  //   src.onmessage = (e) => {
  //     const message = JSON.parse(e.data)

  //     // Handle STATUS messages
  //     if (message.type === 'status') {
  //       console.log('STATUS:', message.message)
  //       return
  //     }

  //     // Handle PATCH messages
  //     if (message.type === 'patch') {
  //       setUiSpec((prev) => {
  //         const patched = jsonpatch.applyPatch(prev, message.patch, true, false)
  //         return patched.newDocument
  //       })
  //       return
  //     }

  //     console.warn('Unknown SSE message:', message)
  //   }

  //   return () => src.close()
  // }, [])

  const triggerGenerateUI = async (prompt: string) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/submit_prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      const data = await response.json()
      console.log('Generate UI response:', data)

      // trigger SSE connection to receive patches for this job_id
      const src = new EventSource(
        `http://127.0.0.1:8000/trigger_job/${data.job_id}`
      )

      src.addEventListener('end', () => {
        console.log('Stream ended. Closing SSE.')
        src.close()
      })

      src.onmessage = (e) => {
        const message = JSON.parse(e.data)

        // Handle STATUS messages
        if (message.type === 'status') {
          console.log('STATUS:', message.message)
          setLlmStatusMessage(message.message)
          return
        }

        // Handle PATCH messages
        if (message.type === 'patch') {
          setUiSpec((prev) => {
            const patched = jsonpatch.applyPatch(
              prev,
              message.patch,
              true,
              false
            )
            return patched.newDocument
          })
          return
        }

        console.warn('Unknown SSE message:', message)
      }
    } catch (error) {
      console.error('Error generating UI:', error)
    }
  }

  return (
    <>
      <h1>Generative UI Builder</h1>
      <p>LLM Status: {llmStatusMessage}</p>
      {currentUISpec && <Renderer data={currentUISpec} />}
      {/* <Renderer data={server_data} /> */}
      <input
        type="text"
        placeholder="Type your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button onClick={() => triggerGenerateUI(prompt)}>Generate UI</button>
    </>
  )
}

export default App
