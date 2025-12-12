import React, { Fragment } from 'react'

// Import necessary components
import Container from '../components/Container'
import Card from '../components/Card'
import Chart from '../components/Chart'
import Table from '../components/Table'

// ... import other components like Text, Image, List, Button etc.

const Renderer: FC<{ data: any }> = ({ data }) => {
  if (!data || !data.root) {
    return <h1>Loading...</h1>
  }

  const renderNode = (node: any) => {
    console.log('Rendering node:', node) // Debug log
    switch (node.type) {
      case 'root':
        return (
          <>
            {node.children &&
              node.children.map((child: any, index: number) => (
                <Fragment key={index}>{renderNode(child)}</Fragment>
              ))}
          </>
        )
      case 'container':
        return (
          <Container direction={node.direction}>
            {node.children &&
              node.children.map((child: any, index: number) => (
                <Fragment key={index}>{renderNode(child)}</Fragment>
              ))}
          </Container>
        )
      case 'chart':
        return (
          <Chart
            dataKey={node.dataKey}
            x_axis={node.x_axis}
            y_axis={node.y_axis}
          ></Chart>
        )
      case 'card':
        return <Card title={node.title} content={node.content}></Card>
      case 'text': {
        // Inline variants → span
        const inlineVariants = [
          'span',
          'span-bold',
          'span-italic',
          'span-underline',
        ]

        // Determine element tag
        let Tag: any = 'span'
        if (node.variant === 'header') Tag = 'h1'
        else if (node.variant === 'subheader') Tag = 'h2'
        else if (node.variant === 'paragraph') Tag = 'p'
        else if (inlineVariants.includes(node.variant)) Tag = 'span'

        // Determine class styles
        const variantClassMap = {
          span: '',
          'span-bold': 'font-bold',
          'span-italic': 'italic',
          'span-underline': 'underline',
          paragraph: 'text-base',
          header: 'text-2xl font-bold',
          subheader: 'text-xl font-semibold',
        } as const

        const className =
          variantClassMap[node.variant as keyof typeof variantClassMap] || ''
        // ...existing code...

        // Render `value` (simple) or `children` (nested)
        if (node.value !== undefined && node.value !== null) {
          return <Tag className={className}>{node.value}</Tag>
        }

        if (node.children) {
          return (
            <Tag className={className}>
              {node.children.map((child: any, index: number) => (
                <Fragment key={index}>{renderNode(child)}</Fragment>
              ))}
            </Tag>
          )
        }

        return null
      }

      case 'image':
        return <img src={node.src} alt={node.alt} />
      case 'list':
        return (
          <div className="list">
            {node.children &&
              node.children.map((item: any, index: number) => (
                <Fragment key={index}>{renderNode(item)}</Fragment>
              ))}
          </div>
        )
      case 'button':
        return (
          <button onClick={() => console.log(node.action)}>{node.label}</button>
        )

      case 'table':
        return <Table dataKey={node.dataKey} />
      default:
        return <pre>{JSON.stringify(node, null, 2)}</pre>
    }
  }
  try {
    return <>{renderNode(data.root)}</>
  } catch (e) {
    return <h1>Loading...</h1>
  }
}

export default Renderer
